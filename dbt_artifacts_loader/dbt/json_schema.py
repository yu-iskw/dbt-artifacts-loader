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
from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass, fields, Field, field
import inspect


@dataclass
class JsonSchema:
    type: str
    format: Optional[str] = None
    pattern: Optional[str] = None
    title: Optional[str] = None
    # id: Optional[str] = field(init=False)
    # schema: Optional[str] = field(init=False)
    required: Optional[List[str]] = None
    additionalProperties: Optional[Union[bool, str, "JsonSchema"]] = None
    description: Optional[str] = None
    properties: Optional[Dict[str, "JsonSchema"]]
    oneOf: Optional[List["JsonSchema"]]
    definitions: Optional[Dict[str, Any]]
    #default: Optional[Union[str, bool, List[Any], Dict[str, Any]]]

    # def __init__(self, **kwargs):
    #     names = set([f.name for f in fields(self)])
    #     for k, v in kwargs.items():
    #         if k in names:
    #             setattr(self, k, v)

    @classmethod
    def from_dict(cls, parameters):
        return cls(**{
            k.replace("$", "'"): v for k, v in parameters.items()
            if k.replace("$", "") in inspect.signature(cls).parameters
        })


# def to_bigquery_schema(json_schema: JsonSchema):
#     if type in [string]:
