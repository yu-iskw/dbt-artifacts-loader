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
from enum import Enum
from typing import Dict, Any, Optional, Union, List
from datetime import datetime
import inspect

from deepmerge import always_merger

from pydantic import BaseModel
from pydantic.fields import ModelField

from google.cloud import bigquery


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


def is_list_type(model_field: ModelField) -> str:
    if typing.get_origin(model_field.outer_type_) is list:
        return True
    return False


def is_union(outer_type_) -> bool:
    if typing.get_origin(outer_type_) is Union:
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
    return [x for x in union_type.__args__ if not is_none_type(x)]


def to_bigquery_schema(model_field: ModelField, depth: int):
    # Primitive data type
    print("start to_bigquery_schema", depth)
    if get_primitive_field_type(outer_type_=model_field.outer_type_) is not None:
        print("primitive")
        return from_simple_type(model_field=model_field)
    # A subclass of the base model
    elif BaseBigQueryModel.issubclass(model_field.outer_type_):
        print("issubclass")
        fields = model_field.outer_type_.to_bigquery_schema(depth=depth + 1)
        return bigquery.SchemaField(
            name=model_field.name,
            description=model_field.field_info.description,
            mode="REPEATED",
            field_type="RECORD",
            fields=fields,
        )
    # Union
    elif is_union_type(model_field=model_field):
        return convert_union_to_schema_field(union_type=model_field.outer_type_,
                                             name=model_field.name,
                                             description=model_field.field_info.description,
                                             depth=depth + 1)
    # ARRAY
    elif is_list_type(model_field=model_field):
        print("is_list_type")
        return from_list_type(model_field=model_field, depth=depth + 1)
    # STRUCT
    elif is_dict_type(model_field=model_field):
        print("is_dict_type")
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
        mode=is_required(model_field=model_field),
        description=model_field.field_info.description,
    )


def from_list_type(model_field: ModelField, depth: int):
    print(model_field.name)
    args = model_field.outer_type_.__args__
    fields = []
    for x in args:
        field = None
        if get_primitive_field_type(outer_type_=x) is not None:
            field = bigquery.SchemaField(
                name=model_field.name,
                mode=is_required(model_field=model_field),
                field_type=get_primitive_field_type(outer_type_=x),
            )
        elif is_union_type(model_field=model_field):
            types_in_union = model_field.outer_type_.__args__
            if all(BaseBigQueryModel.issubclass(x) for x in types_in_union):
                fields = [x.to_bigquery_schema(depth=depth + 1) for x in types_in_union]
                field = bigquery.SchemaField(
                    name=model_field.name,
                    mode="RECORD",
                    field_type="REPEATED",
                    fields=fields,
                )
            else:
                raise ValueError(dir(model_field))
        elif x is ModelField and is_list_type(model_field=x):
            field = to_bigquery_schema(model_field=x, depth=depth + 1)
        elif BaseBigQueryModel.issubclass(x):
            field = x.to_bigquery_schema(depth=depth + 1)
        if field is not None:
            fields.append(field)
    return bigquery.SchemaField(
        name=model_field.name,
        description=model_field.field_info.description,
        field_type="RECORD",
        mode="REPEATED",
        fields=fields,
    )


def from_dict_type(model_field: ModelField, depth: int):
    dict_value_type = get_dict_value_type(model_field=model_field)
    if model_field.outer_type_ is Dict[str, str]:
        print("Dict[str, str]")
        schema_field = bigquery.SchemaField(
            name=model_field.name,
            field_type="RECORD",
            mode="REPEATED",
            fields=[
                bigquery.SchemaField(name="key", field_type="STRING", mode="REQUIRED"),
                bigquery.SchemaField(name="value", field_type="STRING", mode="REQUIRED"),
            ],
            description=model_field.field_info,
        )
        return schema_field
    elif model_field.outer_type_ is Dict[str, Any]:
        print("Dict[str, Any]")
        schema_field = bigquery.SchemaField(
            name=model_field.name,
            field_type=bigquery.StandardSqlDataTypes.STRING.name,
            mode=is_required(model_field=model_field),
            description=model_field.field_info.description,
        )
        return schema_field
    elif model_field.outer_type_ is Dict[str, List[str]]:
        schema_field = bigquery.SchemaField(
            name=model_field.name,
            field_type="RECORD",
            mode="REPEATED",
            fields=[
                bigquery.SchemaField(name="key", field_type="STRING", mode="REQUIRED"),
                bigquery.SchemaField(name="value", field_type="STRING", mode="REPEATED"),
            ],
            description=model_field.field_info,
        )
        return schema_field
    elif (dict_value_type is not None
          and BaseBigQueryModel.issubclass(dict_value_type)):
        fields = dict_value_type.to_bigquery_schema(depth=depth + 1)
        schema_field = bigquery.SchemaField(
            name=model_field.name,
            field_type="RECORD",
            mode="REPEATED",
            fields=[
                bigquery.SchemaField(name="key", field_type="STRING", mode="REQUIRED"),
                bigquery.SchemaField(name="value", field_type="RECORD", mode="REPEATED", fields=fields),
            ],
            description=model_field.field_info,
        )
        return schema_field
    elif dict_value_type is not None and is_union(dict_value_type):
        return convert_union_to_schema_field(
            union_type=dict_value_type,
            name=model_field.name,
            description=model_field.field_info.description,
            depth=depth + 1)
    else:
        raise ValueError(model_field)


def convert_union_to_schema_field(union_type, name: str, description: str, depth: int):
    nested_types = get_nested_types_in_union(union_type=union_type)
    if all([BaseBigQueryModel.issubclass(x) for x in nested_types]):
        print("yyyyyyyyyyyyyyy")
        return bigquery.SchemaField(
            name=name,
            description=description,
            field_type="RECORD",
            mode="REPEATED",
            fields=[
                bigquery.SchemaField(
                    name=sub_type.get_class_name(),
                    field_type="RECORD",
                    mode="REPEATED",
                    fields=sub_type.to_bigquery_schema(depth=depth + 1)
                ) for sub_type in nested_types]
        )
    elif all([get_primitive_field_type(x) is not None for x in nested_types]):
        schema_fields = [
            bigquery.SchemaField(
                name=name,
                field_type=get_primitive_field_type(x),
                mode="NULLABLE",
                description=description,
            )
            for x in union_type.__args__]
        print("zzzzzzzzzzzzzzzzzzzzzz")
        return merge_schema_field(schema_fields=schema_fields)
    elif all([x is List[str] or x is str] for x in nested_types):
        # For `tags`
        schema_fields = bigquery.SchemaField(
            name=name,
            field_type="STRING",
            mode="REPEATED",
            description=description,
        )
        return schema_fields
    else:
        print(union_type)
        for x in union_type:
            print("%%%%%%%%%%%%%%%")
            print(x)
            print(BaseBigQueryModel.issubclass(x))
        raise ValueError(union_type)


class BaseBigQueryModel(BaseModel):

    @classmethod
    def issubclass(cls, x: Any) -> bool:
        if inspect.isclass(x) and issubclass(x, cls):
            return True
        return False

    @classmethod
    def get_class_name(cls) -> str:
        return cls.__name__

    @classmethod
    def to_bigquery_schema(cls, depth: int = 0):
        print("zzzzzzzzzzzz")
        print(cls.__name__, depth)
        fields: Dict[str, ModelField] = cls.__fields__
        schema_fields = []
        for key, model_field in fields.items():
            print("=============")
            print(key)
            print(model_field.outer_type_)
            x = to_bigquery_schema(model_field=model_field, depth=depth)
            print("################")
            schema_fields.append(x)
        return schema_fields
