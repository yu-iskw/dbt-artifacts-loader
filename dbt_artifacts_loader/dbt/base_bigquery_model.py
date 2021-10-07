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
import copy
import typing
import json
from enum import Enum
from typing import Dict, Any, Optional, Union, List
from datetime import datetime, date
import inspect

from deepmerge import always_merger

from pydantic import BaseModel
from pydantic.fields import ModelField

from google.cloud import bigquery

from dbt_artifacts_loader.dbt.utils import datetime_handler


def is_required(model_field: ModelField) -> str:
    if model_field.required is True:
        return "REQUIRED"
    return "NULLABLE"


def has_fields(model_field: ModelField) -> bool:
    return hasattr(model_field, "outer_type_") and hasattr(model_field.outer_type_, "__fields__")


def is_constr(outer_type_) -> bool:
    if (hasattr(outer_type_, "__name__")
            and outer_type_.__name__ == "ConstrainedStrValue"):
        return True
    return False


def is_enum(outer_type_) -> bool:
    if inspect.isclass(outer_type_) and issubclass(outer_type_, Enum):
        return True
    return False


def is_none_type(x):
    if hasattr(x, "__name__") and x.__name__ == "NoneType":
        return True
    return False


def is_list_type(model_field: ModelField) -> bool:
    if typing.get_origin(model_field.outer_type_) is list:
        return True
    return False


def is_union(outer_type_) -> bool:
    if outer_type_ is not None and typing.get_origin(outer_type_) is Union:
        return True
    return False


def is_union_type(model_field: ModelField) -> bool:
    if is_union(outer_type_=model_field.outer_type_):
        return True
    return False


def is_dict_type(model_field: ModelField):
    if (typing.get_origin(model_field.outer_type_) is Dict
            or typing.get_origin(model_field.outer_type_) is dict):
        return True
    return False


def get_all_enum_values(enum_class: Enum) -> list:
    return [x.value for x in enum_class]


def get_primitive_field_type(outer_type_) -> Optional[str]:
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
    elif is_constr(outer_type_=outer_type_):
        return bigquery.StandardSqlDataTypes.STRING.name
    elif type(outer_type_) is typing.TypeVar:
        # This is a workaround for List[List]] or List[List[Any]]
        return bigquery.StandardSqlDataTypes.STRING.name
    elif is_enum(outer_type_=outer_type_):
        return bigquery.StandardSqlDataTypes.STRING.name
    return None


def get_dict_value_type(model_field: ModelField):
    if is_dict_type(model_field=model_field):
        return model_field.outer_type_.__args__[1]
    return None


def get_nested_types_in_union(union_type):
    if hasattr(union_type, "__args__"):
        return [x for x in union_type.__args__ if not is_none_type(x)]
    return None


def get_description(model_field: ModelField):
    """get the field description"""
    field_description = ""
    enum_description = ""
    if is_enum(outer_type_=model_field.outer_type_):
        enum_description = '(one of {})'.format(', '.join(get_all_enum_values(enum_class=model_field.outer_type_)))
    elif model_field.field_info.description is not None:
        field_description = model_field.field_info.description
    return "{} {}".format(field_description, enum_description)


def to_bigquery_schema(model_field: ModelField, depth: int) -> bigquery.SchemaField:
    # Primitive data type
    if get_primitive_field_type(outer_type_=model_field.outer_type_) is not None:
        return from_simple_type(model_field=model_field)
    # A subclass of the base model
    elif BaseBigQueryModel.is_subclass(model_field.outer_type_):
        fields = model_field.outer_type_.to_bigquery_schema(depth=depth + 1)
        return bigquery.SchemaField(
            name=model_field.name,
            description=get_description(model_field=model_field),
            mode="NULLABLE",
            field_type="RECORD",
            fields=fields,
        )
    # Union
    elif is_union_type(model_field=model_field):
        return convert_union_type_to_schema_field(union_type=model_field.outer_type_,
                                                  name=model_field.name,
                                                  description=get_description(model_field=model_field),
                                                  depth=depth + 1)
    # ARRAY
    elif is_list_type(model_field=model_field):
        return from_list_type(model_field=model_field, depth=depth + 1)
    # STRUCT
    elif is_dict_type(model_field=model_field):
        return from_dict_type(model_field=model_field, depth=depth + 1)
    else:
        raise ValueError(model_field)


def merge_schema_field(schema_fields: List[bigquery.SchemaField]) -> bigquery.SchemaField:
    api_representations = [x.to_api_repr() for x in schema_fields]
    base_api_representation = copy.deepcopy(api_representations[0])
    for api_representation in range(1, len(api_representations)):
        always_merger.merge(base_api_representation, api_representation)
    return bigquery.SchemaField.from_api_repr(base_api_representation)


def from_simple_type(model_field: ModelField):
    return bigquery.SchemaField(
        name=model_field.name,
        field_type=get_primitive_field_type(outer_type_=model_field.outer_type_),
        # mode=is_required(model_field=model_field),
        mode="NULLABLE",
        description=get_description(model_field=model_field),
    )


def from_list_type(model_field: ModelField, depth: int) -> bigquery.SchemaField:
    # Get the nested data type in the list
    args = model_field.outer_type_.__args__
    if len(args) > 1:
        raise ValueError(args)

    type_in_list = args[0]
    if get_primitive_field_type(outer_type_=type_in_list) is not None:
        return bigquery.SchemaField(
            name=model_field.name,
            mode="REPEATED",
            field_type=get_primitive_field_type(outer_type_=type_in_list),
            description=get_description(model_field=model_field),
        )
    elif type_in_list is ModelField and is_list_type(model_field=type_in_list):
        return to_bigquery_schema(model_field=type_in_list, depth=depth + 1)
    elif BaseBigQueryModel.is_subclass(type_in_list):
        return bigquery.SchemaField(
            name=model_field.name,
            mode="REPEATED",
            field_type="RECORD",
            description=get_description(model_field=model_field),
            fields=type_in_list.to_bigquery_schema(depth=depth + 1)
        )
    elif is_union_type(model_field=model_field):
        types_in_union = get_nested_types_in_union(union_type=model_field.outer_type_)
        if all(BaseBigQueryModel.is_subclass(x) for x in types_in_union):
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
          and get_primitive_field_type(outer_type_=type_in_list.__args__[0]) is not None):
        # List[List[str]] or List[List[]]
        schema_field = bigquery.SchemaField(
            name=model_field.name,
            mode="REPEATED",
            field_type="RECORD",
            description=get_description(model_field=model_field),
            fields=[
                # NOTE bigQuery doesn't allow us to have nullable array
                bigquery.SchemaField(name="values",
                                     mode="NULLABLE",
                                     field_type="RECORD",
                                     description="NOTE: The column must be complicated, because BigQuery doesn't allow us to have a nullable array.",
                                     fields=[
                                         bigquery.SchemaField(
                                             name="value",
                                             mode="REPEATED",
                                             field_type=get_primitive_field_type(type_in_list.__args__[0]),
                                         )
                                     ])
            ]
        )
        return schema_field
    elif is_union(outer_type_=type_in_list):
        schema_field = convert_union_type_to_schema_field(
            union_type=type_in_list,
            name=model_field.name,
            description=get_description(model_field=model_field),
            depth=depth + 1)
        return schema_field
    else:
        raise ValueError(model_field)


def from_dict_type(model_field: ModelField, depth: int):
    dict_value_type = get_dict_value_type(model_field=model_field)
    if model_field.outer_type_ is Dict[str, str]:
        schema_field = bigquery.SchemaField(
            name=model_field.name,
            field_type="RECORD",
            mode="REPEATED",
            fields=[
                bigquery.SchemaField(name="key", field_type="STRING", mode="NULLABLE"),
                bigquery.SchemaField(name="value", field_type="STRING", mode="NULLABLE"),
            ],
            description=get_description(model_field=model_field),
        )
        return schema_field
    elif model_field.outer_type_ is Dict[str, Any]:
        schema_field = bigquery.SchemaField(
            name=model_field.name,
            field_type=bigquery.StandardSqlDataTypes.STRING.name,
            # mode=is_required(model_field=model_field),
            mode="NULLABLE",
            description="[raw JSON string] {}".format(get_description(model_field=model_field)),
        )
        return schema_field
    elif model_field.outer_type_ is Dict[str, List[str]]:
        schema_field = bigquery.SchemaField(
            name=model_field.name,
            field_type="RECORD",
            mode="REPEATED",
            fields=[
                bigquery.SchemaField(name="key", field_type="STRING", mode="NULLABLE"),
                bigquery.SchemaField(name="value", field_type="STRING", mode="REPEATED"),
            ],
            description=get_description(model_field=model_field),
        )
        return schema_field
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
            description=get_description(model_field=model_field),
        )
        return schema_field
    elif is_union(outer_type_=dict_value_type):
        schema_field = bigquery.SchemaField(
            name=model_field.name,
            field_type="RECORD",
            mode="REPEATED",
            fields=[
                bigquery.SchemaField(name="key", field_type="STRING", mode="NULLABLE"),
                convert_union_type_to_schema_field(union_type=dict_value_type,
                                                   name="value",
                                                   description=get_description(model_field=model_field),
                                                   depth=depth + 1)
            ],
            description=get_description(model_field=model_field),
        )
        return schema_field
    else:
        raise ValueError(model_field.outer_type_)


def convert_union_type_to_schema_field(union_type, name: str, description: str, depth: int) -> bigquery.SchemaField:
    nested_types = get_nested_types_in_union(union_type=union_type)
    # union of children classes of BaseBigQueryModel
    if all([BaseBigQueryModel.is_subclass(x) for x in nested_types]):
        schema_field = bigquery.SchemaField(
            name=name,
            description=description,
            field_type="RECORD",
            mode="REPEATED",
            fields=[
                bigquery.SchemaField(name=sub_type.get_class_name(),
                                     field_type="RECORD",
                                     mode="NULLABLE",
                                     fields=sub_type.to_bigquery_schema(depth=depth + 1))
                for sub_type in nested_types]
        )
        return schema_field
    # union of primitive data types
    elif all([get_primitive_field_type(x) is not None for x in nested_types]):
        schema_field = bigquery.SchemaField(
            name=name,
            mode="NULLABLE",
            description=description,
            field_type="STRING",
        )
        return schema_field
    # a special case for `tags`
    elif all([x is List[str] or x is str] for x in nested_types):
        schema_fields = bigquery.SchemaField(
            name=name,
            field_type="STRING",
            mode="REPEATED",
            description=description,
        )
        return schema_fields
    else:
        raise ValueError(union_type)


#
# functions to convert a pydantic class to JSON for the modified JSON schema
#
def adjust_property(property_value: Any, model_field: ModelField, depth: int):
    # Primitive data type
    if property_value is None:
        return None
    elif get_primitive_field_type(outer_type_=model_field.outer_type_) is not None:
        if isinstance(property_value, (datetime, date)):
            return property_value.strftime('%Y-%m-%dT%H:%M:%S')
        elif isinstance(property_value, Enum):
            return property_value.value
        return property_value
    # A subclass of the base model
    elif BaseBigQueryModel.is_subclass(model_field.outer_type_):
        return property_value.to_dict(depth=depth + 1)
    # Union
    elif is_union_type(model_field=model_field):
        return convert_union_object_to_dict(property_value=property_value,
                                            union_type=model_field.outer_type_,
                                            depth=depth + 1)
    # ARRAY
    elif is_list_type(model_field=model_field):
        return adjust_list_property(property_value=property_value, model_field=model_field, depth=depth + 1)
    # STRUCT
    elif is_dict_type(model_field=model_field):
        return adjust_dict_property(property_value=property_value, model_field=model_field, depth=depth + 1)
    else:
        raise ValueError(model_field)


def adjust_list_property(property_value: Any, model_field: ModelField, depth: int):
    # Get the nested data type in the list
    args = model_field.outer_type_.__args__
    if len(args) > 1:
        raise ValueError(args)

    type_in_list = args[0]
    # primitive type
    if get_primitive_field_type(outer_type_=type_in_list) is not None:
        return property_value
    # a list of lists
    elif type_in_list is ModelField and is_list_type(model_field=type_in_list):
        return [adjust_property(property_value=x, model_field=type_in_list, depth=depth + 1)
                for x in property_value]
    elif BaseBigQueryModel.is_subclass(type_in_list):
        return [x.to_dict(depth=depth + 1) for x in property_value]
    # a list of primitive data types
    elif (typing.get_origin(type_in_list) is list
          and get_primitive_field_type(outer_type_=type_in_list.__args__[0]) is not None):
        return [{"values": {"value": x}} for x in property_value]
    # one of Union
    elif is_union(outer_type_=type_in_list):
        return [
            convert_union_object_to_dict(property_value=x, union_type=type_in_list, depth=depth + 1)
            for x in property_value]
    else:
        raise ValueError(model_field)


def adjust_dict_property(property_value: Any, model_field: ModelField, depth: int):
    dict_value_type = get_dict_value_type(model_field=model_field)
    if model_field.outer_type_ is Dict[str, str]:
        return [{"key": k, "value": v} for k, v in property_value.items()]
    elif model_field.outer_type_ is Dict[str, Any]:
        # Convert the dictionary to the JSON string
        return json.dumps(property_value, default=datetime_handler)
    elif model_field.outer_type_ is Dict[str, List[str]]:
        return [{"key": k, "value": v} for k, v in property_value.items()]
    elif BaseBigQueryModel.is_subclass(dict_value_type):
        return [{"key": k, "value": v.to_dict(depth=depth + 1)} for k, v in property_value.items()]
    elif is_union(outer_type_=dict_value_type):
        return [{
            "key": k,
            "value": convert_union_object_to_dict(property_value=v, union_type=dict_value_type, depth=depth + 1)
        } for k, v in property_value.items()]
    else:
        raise ValueError(model_field.outer_type_)


def convert_union_object_to_dict(property_value: Any, union_type, depth: int):
    nested_types = get_nested_types_in_union(union_type=union_type)
    if all([BaseBigQueryModel.is_subclass(x) for x in nested_types]):
        return {
            property_value.__class__.get_class_name(): property_value.to_dict(depth=depth + 1)
        }
    elif all([get_primitive_field_type(x) is not None for x in nested_types]):
        return [str(x) for x in property_value]
    # a special case for `tags`
    elif all([x is List[str] or x is str] for x in nested_types):
        if type(property_value) is str:
            return [property_value]
        return property_value
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
        return cls.__name__

    @classmethod
    def get_fields(cls) -> Dict[str, ModelField]:
        return cls.__fields__

    @classmethod
    def get_property_type(cls, property_name):
        return cls.__fields__.get(property_name)

    @classmethod
    def to_bigquery_schema(cls, depth: int = 0):
        fields = cls.get_fields()
        schema_fields = []
        for key, model_field in fields.items():
            x = to_bigquery_schema(model_field=model_field, depth=depth + 1)
            schema_fields.append(x)
        return schema_fields

    def to_dict(self, depth: int) -> dict:
        fields = self.__class__.get_fields()
        arranged_dict = {}
        for key, model_field in fields.items():
            arranged_dict[key] = adjust_property(property_value=getattr(self, key),
                                                 model_field=model_field,
                                                 depth=depth + 1)
        return arranged_dict
