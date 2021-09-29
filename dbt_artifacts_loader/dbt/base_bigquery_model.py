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
import io
import typing
from pprint import pprint
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass

from datetime import datetime

import pydantic.types
from pydantic import BaseModel
from pydantic.fields import ModelField

from google.cloud import bigquery


def is_required(model_field: ModelField):
    if model_field.required is True:
        return "REQUIRED"
    return "NULLABLE"


def has_fields(model_field: ModelField):
    return hasattr(model_field, "outer_type_") and hasattr(model_field.outer_type_, "__fields__")


def is_constr(model_field: ModelField):
    if (hasattr(model_field.outer_type_, "__name__")
            and model_field.outer_type_.__name__ == "ConstrainedStrValue"):
        return True
    return False


def get_primitive_field_type(model_field: ModelField) -> str:
    if model_field.outer_type_ is bool:
        return bigquery.StandardSqlDataTypes.BOOL.name
    elif model_field.outer_type_ is str:
        return bigquery.StandardSqlDataTypes.STRING.name
    elif model_field.outer_type_ is float:
        return bigquery.StandardSqlDataTypes.FLOAT64.name
    elif model_field.outer_type_ is datetime:
        return bigquery.StandardSqlDataTypes.DATETIME.name
    elif is_constr(model_field=model_field):
        return bigquery.StandardSqlDataTypes.STRING.name
    else:
        return None


def is_list(model_field: ModelField):
    if typing.get_origin(model_field.outer_type_) is list:
        return True
    return False


def is_union(model_field: ModelField):
    if typing.get_origin(model_field.outer_type_) is Union:
        return True
    return False


def is_dict(model_field: ModelField):
    if typing.get_origin(model_field.outer_type_) is Dict:
        return True
    return False


def to_bigquery_schema(modelf_field: ModelField):
    # Primitive data type
    if get_primitive_field_type(model_field=modelf_field) is not None:
        return to_primitive_type(model_field=modelf_field)
    # ARRAY
    if is_list(model_field=modelf_field):
        return to_array_type(model_field=modelf_field)
    # STRUCT
    if is_dict(model_field=modelf_field):
    return None


def to_primitive_type(model_field: ModelField):
    return bigquery.SchemaField(
        name=model_field.name,
        field_type=get_primitive_field_type(model_field=model_field),
        mode=is_required(model_field=model_field),
        description=model_field.field_info.description,
    )


def to_array_type(model_field: ModelField):
    args = model_field.outer_type_.__args__
    for x in args:
        to_bigquery_schema(modelf_field=x)


class BaseBigQueryModel(BaseModel):

    @classmethod
    def to_bigquery_schema(cls):
        fields: Dict[str, ModelField] = cls.__fields__
        print("=============")
        schema_fields = []
        for key, model_field in fields.items():
            print(key)
            schema_field = None
            primitive_data_type = get_primitive_field_type(model_field=model_field)
            if primitive_data_type is not None:
                schema_field = bigquery.SchemaField(
                    name=model_field.name,
                    field_type=primitive_data_type,
                    mode=is_required(model_field=model_field),
                    description=model_field.field_info.description,
                )
            elif has_fields(model_field=model_field):
                schema_field = bigquery.SchemaField(
                    name = model_field.name,
                    field_type="RECORD",
                    mode="REPEATED",
                    fields=[],
                )
            elif is_list(model_field=model_field):
                for x in model_field.outer_type_.__args__:
                    if get_primitive_field_type(x.outer_type_) is not None:
                        foo = bigquery.SchemaField(
                            name=model_field.name,
                            field_type=get_primitive_field_type(x.outer_type_),
                            mode=is_required(model_field=model_field),
                        )
                    elif is_list(x):
                        print(x)
            elif model_field.outer_type_ is List[str]:
                schema_field = bigquery.SchemaField(
                    name=model_field.name,
                    field_type="STRING",
                    mode="REPEATED",
                )
            elif model_field.outer_type_ is Dict[str, Any]:
                schema_field = bigquery.SchemaField(
                    name=model_field.name,
                    field_type=bigquery.StandardSqlDataTypes.STRING.name,
                    mode=is_required(model_field=model_field),
                    #description="JSON object as STRING",
                )
            elif model_field.outer_type_ is Dict[str, str]:
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

            print("============")
            print(model_field.outer_type_)
            print(model_field.type_)
            print()
            if hasattr(model_field.outer_type_, "__args__"):
                print(model_field.outer_type_.__args__)
            if schema_field is not None:
                schema_fields.append(schema_field)
        pprint(schema_fields)
        return schema_fields
