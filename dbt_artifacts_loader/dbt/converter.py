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
from dataclasses import dataclass
from typing import Optional, Union, Dict, Any

from pydantic import BaseModel
from pydantic.fields import ModelField


def expand_model_field(model_field: ModelField):
    """Expand the field."""
    if has_subfields(model_field=model_field):
        return {k: expand_model_field(v) for k, v in model_field.outer_type_.__fields__.items()}
    if is_union_type(model_field=model_field):
        return expand_type(model_field=model_field)
    return model_field


def expand_type(model_field: ModelField):
    if is_union_type(model_field=model_field):
        nested_types = get_nested_types(model_field=model_field)
        return [expand_model_field(x) for x in nested_types]


def has_subfields(model_field: ModelField):
    """Check if the field has sub fields."""
    return hasattr(model_field.outer_type_, "__fields__")


def is_union_type(model_field: ModelField):
    """Check if the field is a union type."""
    return hasattr(model_field.type_, "__args__")


def get_nested_types(model_field: ModelField):
    return model_field.type_.__args__
