#
#  Licensed to the Apache Software Foundation (ASF) under one or more
#  contributor license agreements.  See the NOTICE file distributed with
#  this work for additional information regarding copyright ownership.
#  The ASF licenses this file to You under the Apache License, Version 2.0
#  (the "License"); you may not use this file except in compliance with
#  the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import datetime
import inspect
import json
import typing
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

# pylint: disable=E0611
import typing_extensions
from google.cloud import bigquery
from pydantic import BaseModel
from pydantic.fields import ModelField


def datetime_handler(x):
    """The handler is used to deal with date and datetime"""
    if isinstance(x, (datetime.datetime, datetime.date, datetime, date)):
        return x.isoformat()
    raise TypeError(f'Type {type(x)} not serializable')


class TypingUtils:
    @staticmethod
    def is_constr(outer_type_) -> bool:
        """Check if it is constr or not"""
        if (hasattr(outer_type_, "__name__")
                and outer_type_.__name__ == "ConstrainedStrValue"):
            return True
        return False

    @staticmethod
    def is_list(outer_type_) -> bool:
        """Check if it is a list or not"""
        if typing_extensions.get_origin(outer_type_) is list:
            return True
        return False

    @staticmethod
    def is_enum(outer_type_) -> bool:
        """Check if it is a subclass of `Enum` or not"""
        if inspect.isclass(outer_type_) and issubclass(outer_type_, Enum):
            return True
        # pylint: disable=unidiomatic-typecheck
        if type(outer_type_) == Enum:
            return True
        return False

    @staticmethod
    def is_none_type(x):
        """Check if it is `Nonetype` or not"""
        if hasattr(x, "__name__") and x.__name__ == "NoneType":
            return True
        return False

    @staticmethod
    def is_union(outer_type_) -> bool:
        """Check if it is `Union[...]` or not"""
        if outer_type_ is not None and typing.get_origin(outer_type_) is Union:
            return True
        return False

    @staticmethod
    def get_nested_types_in_list(union_type):
        """Get the nested data types in List
        e.g. List[str] => str
        """
        if hasattr(union_type, "__args__") and not TypingUtils.is_none_type(union_type):
            return union_type.__args__[0]
        return None

    @staticmethod
    def get_nested_types_in_union(union_type):
        """Get the nested data types in Union
        e.g. Union[str, List[str], NoneType] => [str, List[str]]
        """
        if hasattr(union_type, "__args__"):
            return [x for x in union_type.__args__ if not TypingUtils.is_none_type(x)]
        return None

    @staticmethod
    def get_primitive_field_type(outer_type_) -> Optional[str]:
        """Get a primitive BigQuery field type by data type"""
        if outer_type_ is bool:
            return bigquery.StandardSqlDataTypes.BOOL.name
        elif outer_type_ is str:
            return bigquery.StandardSqlDataTypes.STRING.name
        elif outer_type_ is int:
            return bigquery.StandardSqlDataTypes.INT64.name
        elif outer_type_ is float:
            return bigquery.StandardSqlDataTypes.FLOAT64.name
        elif outer_type_ is datetime:
            return bigquery.StandardSqlDataTypes.DATETIME.name
        elif TypingUtils.is_constr(outer_type_=outer_type_):
            # Corresponding to `pydantic.constr`
            return bigquery.StandardSqlDataTypes.STRING.name
        elif type(outer_type_) is typing.TypeVar:  # pylint: disable=C0123
            # This is a workaround for List[List]] or List[List[Any]]
            return bigquery.StandardSqlDataTypes.STRING.name
        elif TypingUtils.is_enum(outer_type_=outer_type_):
            return bigquery.StandardSqlDataTypes.STRING.name
        return None


class ModelFieldUtils:
    @staticmethod
    def is_required(model_field: ModelField) -> str:
        """Check if model_field is required or not"""
        if model_field.required is True:
            return "REQUIRED"
        return "NULLABLE"

    @staticmethod
    def has_fields(model_field: ModelField) -> bool:
        """Check if `outer_type_` of the model_field has `__fields__` or not"""
        return (hasattr(model_field, "outer_type_")
                and hasattr(model_field.outer_type_, "__fields__")
                and len(model_field.outer_type_.__fields__) > 0)

    @staticmethod
    def is_list_type(model_field: ModelField) -> bool:
        """Check if it is a list or not"""
        if typing.get_origin(model_field.outer_type_) is list:
            return True
        return False

    @staticmethod
    def is_union_type(model_field: ModelField) -> bool:
        """Check if the model_field has `Union[...]` or not"""
        if TypingUtils.is_union(outer_type_=model_field.outer_type_):
            return True
        return False

    @staticmethod
    def is_dict_type(model_field: ModelField):
        """Check if the model_field is a dict or not"""
        if (typing.get_origin(model_field.outer_type_) is Dict
                or typing.get_origin(model_field.outer_type_) is dict):
            return True
        return False

    @staticmethod
    def get_dict_value_type(model_field: ModelField):
        """Get the data type of value of the dictionary.
        e.g. Dict[str, List[str]] => List[str]
        """
        if ModelFieldUtils.is_dict_type(model_field=model_field):
            return model_field.outer_type_.__args__[1]
        return None

    @staticmethod
    def get_description(model_field: ModelField):
        """get the field description"""
        field_description = ""
        enum_description = ""
        if TypingUtils.is_enum(outer_type_=model_field.outer_type_):
            enum_description = '(one of {})'.format(', '.join(get_all_enum_values(enum_class=model_field.outer_type_)))
        elif model_field.field_info.description is not None:
            field_description = model_field.field_info.description
        return "{} {}".format(field_description, enum_description).strip()


def get_all_enum_values(enum_class: Enum) -> list:
    """Get all values in the `Enum` class"""
    return [x.value for x in enum_class]


def to_bigquery_schema(model_field: ModelField, depth: int) -> bigquery.SchemaField:
    """Convert the model_field to SchemaField"""
    # Primitive data type
    if TypingUtils.get_primitive_field_type(outer_type_=model_field.outer_type_) is not None:
        return from_simple_type(model_field=model_field)
    # A subclass of the base model
    elif BaseBigQueryModel.is_subclass(model_field.outer_type_):
        # Special case like Strategy2 in dbt_artifacts_loader.dbt.v1.manifest.py
        if ModelFieldUtils.has_fields(model_field=model_field) is False:
            return bigquery.SchemaField(
                name=model_field.name,
                description=ModelFieldUtils.get_description(model_field=model_field),
                field_type="STRING",
                mode="NULLABLE",
            )
        # Dig into the sub class
        fields = model_field.outer_type_.to_bigquery_schema(depth=depth + 1)
        return bigquery.SchemaField(
            name=model_field.name,
            description=ModelFieldUtils.get_description(model_field=model_field),
            mode="NULLABLE",
            field_type="RECORD",
            fields=fields,
        )
    # Union
    elif ModelFieldUtils.is_union_type(model_field=model_field):
        return convert_union_type_to_schema_field(
            union_type=model_field.outer_type_,
            name=model_field.name,
            description=ModelFieldUtils.get_description(model_field=model_field),
            depth=depth + 1)
    # ARRAY
    elif ModelFieldUtils.is_list_type(model_field=model_field):
        return from_list_type(model_field=model_field, depth=depth + 1)
    # STRUCT
    elif ModelFieldUtils.is_dict_type(model_field=model_field):
        return from_dict_type(model_field=model_field, depth=depth + 1)
    else:
        raise ValueError(model_field)


# If we need something like the function, we re-implement it.
# def merge_schema_field(schema_fields: List[bigquery.SchemaField]) -> bigquery.SchemaField:
#     api_representations = [x.to_api_repr() for x in schema_fields]
#     base_api_representation = copy.deepcopy(api_representations[0])
#     for api_representation in range(1, len(api_representations)):
#         always_merger.merge(base_api_representation, api_representation)
#     return bigquery.SchemaField.from_api_repr(base_api_representation)


def from_simple_type(model_field: ModelField):
    """Convert a simple data type to SchemaField"""
    return bigquery.SchemaField(
        name=model_field.name,
        field_type=TypingUtils.get_primitive_field_type(outer_type_=model_field.outer_type_),
        # mode=is_required(model_field=model_field),
        mode="NULLABLE",
        description=ModelFieldUtils.get_description(model_field=model_field),
    )


def from_list_type(model_field: ModelField, depth: int) -> bigquery.SchemaField:
    """Convert a list data type to SchemaField"""
    # Get the nested data type in the list
    args = model_field.outer_type_.__args__
    if len(args) > 1:
        raise ValueError(args)

    type_in_list = args[0]
    if TypingUtils.get_primitive_field_type(outer_type_=type_in_list) is not None:
        # Make it nullable by default
        return bigquery.SchemaField(
            name=model_field.name,
            field_type="RECORD",
            mode="NULLABLE",
            description=ModelFieldUtils.get_description(model_field=model_field),
            fields=[
                bigquery.SchemaField(
                    name="value",
                    field_type=TypingUtils.get_primitive_field_type(outer_type_=type_in_list),
                    mode="REPEATED",
                    description=ModelFieldUtils.get_description(model_field=model_field),
                )
            ]
        )
    elif type_in_list is ModelField and ModelFieldUtils.is_list_type(model_field=type_in_list):
        return to_bigquery_schema(model_field=type_in_list, depth=depth + 1)
    elif BaseBigQueryModel.is_subclass(type_in_list):
        return bigquery.SchemaField(
            name=model_field.name,
            mode="REPEATED",
            field_type="RECORD",
            description=ModelFieldUtils.get_description(model_field=model_field),
            fields=type_in_list.to_bigquery_schema(depth=depth + 1)
        )
    elif ModelFieldUtils.is_union_type(model_field=model_field):
        types_in_union = TypingUtils.get_nested_types_in_union(union_type=model_field.outer_type_)
        if all(BaseBigQueryModel.is_subclass(x) for x in types_in_union):
            # Forcefully cast to STRING
            schema_field = bigquery.SchemaField(
                name=model_field.name,
                mode="RECORD",
                field_type="REPEATED",
                fields="STRING",
            )
            return schema_field
        else:
            raise ValueError(model_field)
    elif (typing.get_origin(type_in_list) is list
          and TypingUtils.get_primitive_field_type(outer_type_=type_in_list.__args__[0]) is not None):
        # List[List[str]] or List[List[]]
        schema_field = bigquery.SchemaField(
            name=model_field.name,
            mode="REPEATED",
            field_type="RECORD",
            description=ModelFieldUtils.get_description(model_field=model_field),
            fields=[
                # NOTE bigQuery doesn't allow us to have nullable array
                bigquery.SchemaField(
                    name="values",
                    mode="NULLABLE",
                    field_type="RECORD",
                    description="NOTE: The column must be complicated,"
                                "because BigQuery doesn't allow us to have a nullable array.",
                    fields=[
                        bigquery.SchemaField(
                            name="value",
                            mode="REPEATED",
                            field_type=TypingUtils.get_primitive_field_type(type_in_list.__args__[0]),
                        )
                    ])
            ]
        )
        return schema_field
    elif TypingUtils.is_union(outer_type_=type_in_list):
        schema_field = bigquery.SchemaField(
            name=model_field.name,
            field_type="RECORD",
            mode="REPEATED",
            fields=[
                convert_union_type_to_schema_field(
                    union_type=type_in_list,
                    name="values",
                    description=ModelFieldUtils.get_description(model_field=model_field),
                    depth=depth + 1)
            ]
        )
        return schema_field
    else:
        raise ValueError(model_field)


def from_dict_type(model_field: ModelField, depth: int):
    """Convert a dict data type to SchemaField"""
    dict_value_type = ModelFieldUtils.get_dict_value_type(model_field=model_field)
    # Convert to `ARRAY<STRUCT<key STRING, value STRING>>`
    if model_field.outer_type_ is Dict[str, str]:
        schema_field = bigquery.SchemaField(
            name=model_field.name,
            field_type="RECORD",
            mode="REPEATED",
            fields=[
                bigquery.SchemaField(name="key", field_type="STRING", mode="NULLABLE"),
                bigquery.SchemaField(name="value", field_type="STRING", mode="NULLABLE"),
            ],
            description=ModelFieldUtils.get_description(model_field=model_field),
        )
        return schema_field
    # Convert to `STRING` for JSON string
    elif model_field.outer_type_ is Dict[str, Any]:
        schema_field = bigquery.SchemaField(
            name=model_field.name,
            field_type=bigquery.StandardSqlDataTypes.STRING.name,
            # mode=is_required(model_field=model_field),
            mode="NULLABLE",
            description=f"[raw JSON string] {ModelFieldUtils.get_description(model_field=model_field)}".strip(),
        )
        return schema_field
    # Convert to ARRAY<STRUCT<key STRING, value ARRAY<STRING>>>
    elif model_field.outer_type_ is Dict[str, List[str]]:
        schema_field = bigquery.SchemaField(
            name=model_field.name,
            field_type="RECORD",
            mode="REPEATED",
            fields=[
                bigquery.SchemaField(name="key", field_type="STRING", mode="NULLABLE"),
                bigquery.SchemaField(name="value", field_type="STRING", mode="REPEATED"),
            ],
            description=ModelFieldUtils.get_description(model_field=model_field),
        )
        return schema_field
    # Expect Dict[str, List[...]]
    elif TypingUtils.is_list(dict_value_type):
        # Expect Dict[str, List[Union[...]]]
        # pylint: disable=C0103
        _nested_type_in_list = TypingUtils.get_nested_types_in_list(dict_value_type)
        if TypingUtils.is_union(_nested_type_in_list):
            # pylint: disable=C0103
            __nested_type_in_union = TypingUtils.get_nested_types_in_union(_nested_type_in_list)
            # Expect Dict[str, List[Union[BaseBigQueryModel, ...]]]
            if all((BaseBigQueryModel.is_subclass(t) for t in __nested_type_in_union)):
                # pylint: disable=C0103
                __fields = convert_union_type_to_schema_field(union_type=_nested_type_in_list,
                                                              name="values", description="", depth=depth + 1).fields
                schema_field = bigquery.SchemaField(
                    name=model_field.name,
                    field_type="RECORD",
                    mode="REPEATED",
                    fields=[
                        bigquery.SchemaField(name="key", field_type="STRING", mode="NULLABLE"),
                        bigquery.SchemaField(name="values",
                                             field_type="RECORD",
                                             mode="REPEATED",
                                             fields=__fields),
                    ],
                    description=ModelFieldUtils.get_description(model_field=model_field),
                )
                return schema_field
            else:
                raise ValueError(model_field)
        else:
            raise ValueError(model_field)
    # Convert to ARRAY<STRUCT<key STRING, value STRUCT<T>>>
    elif BaseBigQueryModel.is_subclass(dict_value_type):
        fields = dict_value_type.to_bigquery_schema(depth=depth + 1)
        schema_field = bigquery.SchemaField(
            name=model_field.name,
            field_type="RECORD",
            mode="REPEATED",
            fields=[
                bigquery.SchemaField(name="key", field_type="STRING", mode="NULLABLE"),
                bigquery.SchemaField(name="value", field_type="RECORD", mode="NULLABLE", fields=fields),
            ],
            description=ModelFieldUtils.get_description(model_field=model_field),
        )
        return schema_field
    # Convert to ARRAY<STRUCT<key STRING, value T>>
    elif TypingUtils.is_union(outer_type_=dict_value_type):
        schema_field = bigquery.SchemaField(
            name=model_field.name,
            field_type="RECORD",
            mode="REPEATED",
            fields=[
                bigquery.SchemaField(name="key", field_type="STRING", mode="NULLABLE"),
                convert_union_type_to_schema_field(
                    union_type=dict_value_type,
                    name="value",
                    description=ModelFieldUtils.get_description(model_field=model_field),
                    depth=depth + 1)
            ],
            description=ModelFieldUtils.get_description(model_field=model_field),
        )
        return schema_field
    else:
        raise ValueError(model_field.outer_type_)


def convert_union_type_to_schema_field(union_type, name: str, description: str, depth: int) -> bigquery.SchemaField:
    """Convert Union[...] to SchemaField"""
    nested_types = TypingUtils.get_nested_types_in_union(union_type=union_type)
    # union of children classes of BaseBigQueryModel
    # pylint: disable=R1729
    if all([BaseBigQueryModel.is_subclass(x) for x in nested_types]):
        schema_field = bigquery.SchemaField(
            name=name,
            description=description,
            field_type="RECORD",
            mode="NULLABLE",
            fields=[
                bigquery.SchemaField(name=sub_type.get_class_name(),
                                     field_type="RECORD",
                                     mode="NULLABLE",
                                     fields=sub_type.to_bigquery_schema(depth=depth + 1))
                for sub_type in nested_types]
        )
        return schema_field
    # union of primitive data types
    # pylint: disable=R1729
    elif all([TypingUtils.get_primitive_field_type(x) is not None for x in nested_types]):
        schema_field = bigquery.SchemaField(
            name=name,
            mode="NULLABLE",
            description=description,
            field_type="STRING",
        )
        return schema_field
    # List[Union[List[str], str]]
    elif all([x is List[str] or x is str] for x in nested_types):
        # It must be complicated to be nullable.
        schema_fields = bigquery.SchemaField(
            name=name,
            field_type="RECORD",
            mode="NULLABLE",
            description=description,
            fields=[
                bigquery.SchemaField(
                    name="value",
                    field_type="STRING",
                    mode="REPEATED",
                    description=description,
                )
            ],
        )
        return schema_fields
    else:
        raise ValueError(union_type)


#
# functions to convert a pydantic class to JSON for the modified JSON schema
#
def adjust_property(property_value: Any, model_field: ModelField, depth: int):
    """Adjust properties for the BigQuery schema"""
    # Primitive data type
    if property_value is None:
        return None
    elif TypingUtils.get_primitive_field_type(outer_type_=model_field.outer_type_) is not None:
        if isinstance(property_value, (datetime, date)):
            return property_value.strftime('%Y-%m-%dT%H:%M:%S')
        elif isinstance(property_value, Enum):
            return property_value.value
        return property_value
    # A subclass of the base model
    elif BaseBigQueryModel.is_subclass(model_field.outer_type_):
        # Special case like Strategy2 in dbt_artifacts_loader.dbt.v1.manifest.py
        if ModelFieldUtils.has_fields(model_field=model_field) is False:
            return str(property_value)
        return property_value.to_dict(depth=depth + 1)
    # Union
    elif ModelFieldUtils.is_union_type(model_field=model_field):
        return adjust_union_value(property_value=property_value,
                                  union_type=model_field.outer_type_,
                                  depth=depth + 1)
    # ARRAY
    elif ModelFieldUtils.is_list_type(model_field=model_field):
        return adjust_list_property(property_value=property_value, model_field=model_field, depth=depth + 1)
    # STRUCT
    elif ModelFieldUtils.is_dict_type(model_field=model_field):
        return adjust_dict_property(property_value=property_value, model_field=model_field, depth=depth + 1)
    else:
        raise ValueError(model_field)


def adjust_list_property(property_value: Any, model_field: ModelField, depth: int):
    """Convert a list property for the BigQuery schema"""
    # Get the nested data type in the list
    args = model_field.outer_type_.__args__
    if len(args) > 1:
        raise ValueError(args)

    type_in_list = args[0]
    # a list of lists
    if type_in_list is ModelField and ModelFieldUtils.is_list_type(model_field=type_in_list):
        return [adjust_property(property_value=x, model_field=type_in_list, depth=depth + 1)
                for x in property_value]
    elif BaseBigQueryModel.is_subclass(type_in_list):
        return [x.to_dict(depth=depth + 1) for x in property_value]
    # a list of primitive data types
    elif (typing.get_origin(type_in_list) is list
          and TypingUtils.get_primitive_field_type(outer_type_=type_in_list.__args__[0]) is not None):
        return [{"values": {"value": x}} for x in property_value]
    # one of Union
    elif TypingUtils.is_union(outer_type_=type_in_list):
        value = [
            {"values": adjust_union_value(property_value=x, union_type=type_in_list, depth=depth + 1)}
            for x in property_value]
        return value
    # primitive type
    elif TypingUtils.get_primitive_field_type(outer_type_=type_in_list) is not None:
        if TypingUtils.is_enum(type_in_list):
            return {"value": get_all_enum_values(property_value)}
        else:
            return {"value": list(property_value)}
    else:
        raise ValueError(model_field)


def adjust_dict_property(property_value: Any, model_field: ModelField, depth: int):
    """Convert a dict property for the BigQuery schema"""
    dict_value_type = ModelFieldUtils.get_dict_value_type(model_field=model_field)
    # Scalar
    if model_field.outer_type_ is Dict[str, str]:
        return [{"key": k, "value": v} for k, v in property_value.items()]
    elif model_field.outer_type_ is Dict[str, List[str]]:
        return [{"key": k, "value": v} for k, v in property_value.items()]
    elif model_field.outer_type_ is Dict[str, Any]:
        # Convert the dictionary to the JSON string
        return json.dumps(property_value, default=datetime_handler)
    # Expect Dict[str, List[...]]
    elif TypingUtils.is_list(dict_value_type):
        # Expect Dict[str, List[Union[...]]]
        # pylint: disable=C0103
        _nested_type_in_list = TypingUtils.get_nested_types_in_list(dict_value_type)
        if TypingUtils.is_union(_nested_type_in_list):
            # pylint: disable=C0103
            __nested_type_in_union = TypingUtils.get_nested_types_in_union(_nested_type_in_list)
            # Expect Dict[str, List[Union[BaseBigQueryModel, ...]]]
            if all((BaseBigQueryModel.is_subclass(t) for t in __nested_type_in_union)):
                return [{
                    "key": k,
                    "values": [
                        {
                            nested_model.get_class_name(): nested_model.to_dict(depth=depth + 1)
                        }
                        for nested_model in v],
                } for k, v in property_value.items()]
            else:
                raise ValueError(property_value, model_field)
        else:
            raise ValueError(property_value, model_field)
    elif BaseBigQueryModel.is_subclass(dict_value_type):
        return [{"key": k, "value": v.to_dict(depth=depth + 1)} for k, v in property_value.items()]
    elif TypingUtils.is_union(outer_type_=dict_value_type):
        return [{
            "key": k,
            "value": adjust_union_value(property_value=v, union_type=dict_value_type, depth=depth + 1)
        } for k, v in property_value.items()]
    else:
        raise ValueError(property_value, model_field)


def adjust_union_value(property_value: Any, union_type, depth: int):
    """Convert a union property for the BigQuery schema"""
    nested_types = TypingUtils.get_nested_types_in_union(union_type=union_type)
    # pylint: disable=R1729
    if all([BaseBigQueryModel.is_subclass(x) for x in nested_types]):
        return {property_value.__class__.get_class_name(): property_value.to_dict(depth=depth + 1)}
    # pylint: disable=R1729
    elif all([TypingUtils.get_primitive_field_type(x) is not None for x in nested_types]):
        # Forcefully cast to STRING
        if TypingUtils.is_enum(outer_type_=type(property_value)):
            property_value = property_value.value
        return str(property_value)
    # List[Union[List[str], str, None]]
    elif all([x is None or x is List[str] or x is str] for x in nested_types):
        return {"value": list(property_value)}
    else:
        raise ValueError(union_type)


#
# The base class of pydantic classes generated from the JSON schemas
#
class BaseBigQueryModel(BaseModel):

    @classmethod
    def is_subclass(cls, x: Any) -> bool:
        if x is not None and inspect.isclass(x) and issubclass(x, cls):
            return True
        return False

    @classmethod
    def get_class_name(cls) -> str:
        """Get the class name"""
        return cls.__name__

    @classmethod
    def get_fields(cls) -> Dict[str, ModelField]:
        """Get the fields"""
        return cls.__fields__

    @classmethod
    def has_fields(cls) -> bool:
        """Check if the class has field(s) or not."""
        if len(cls.get_fields()) > 0:
            return True
        return False

    @classmethod
    def get_field(cls, name: str) -> ModelField:
        """Get a file by the name"""
        fields = cls.get_fields()
        if name in fields.keys():
            return fields.get(name)
        raise ValueError("name: {} doesn't exist".format(name))

    @classmethod
    def to_bigquery_schema(cls, depth: int = 0):
        """Convert the class to the BigQuery schema"""
        fields = cls.get_fields()
        schema_fields = []
        for _, model_field in fields.items():
            x = to_bigquery_schema(model_field=model_field, depth=depth + 1)
            schema_fields.append(x)
        return schema_fields

    def to_dict(self, depth: int) -> dict:
        """Convert the instance to dict"""
        fields = self.__class__.get_fields()
        arranged_dict = {}
        for key, model_field in fields.items():
            arranged_dict[key] = adjust_property(property_value=getattr(self, key),
                                                 model_field=model_field,
                                                 depth=depth + 1)
        return arranged_dict
