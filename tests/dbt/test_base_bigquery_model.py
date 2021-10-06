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
#
import unittest

from pprint import pprint
import json

from typing import Optional, Dict
from datetime import datetime

from pydantic import Extra

from dbt_artifacts_loader.dbt.base_bigquery_model import BaseBigQueryModel
from dbt_artifacts_loader.dbt.v2 import manifest


class TestMetadata(BaseBigQueryModel):
    class Config:
        extra = Extra.forbid

    dbt_schema_version: Optional[str] = 'https://schemas.getdbt.com/dbt/catalog/v1.json'
    dbt_version: Optional[str] = '0.19.0'
    generated_at: Optional[datetime] = '2021-02-10T04:42:33.680487Z'
    invocation_id: Optional[Optional[str]] = None
    env: Optional[Dict[str, str]] = {}


class TestBaseBigQueryModel(unittest.TestCase):

    # def test_to_bigquery_schema(self):
    #     value = TestMetadata.to_bigquery_schema()
    #     expected = None
    #     self.assertEqual(value, expected)

    def test_to_bigquery_schema2(self):
        value = manifest.Manifest.to_bigquery_schema()
        expected = None
        with open("/tmp/foo.json", "w") as fp:
            data = [x.to_api_repr() for x in value]
            json.dump(data, fp)
        self.assertEqual(value, expected)
