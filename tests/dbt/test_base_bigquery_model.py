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
import os
import unittest
import json

from datetime import datetime
from typing import Optional, Dict

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

    def setUp(self):
        # Load the testing manifest.json
        path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "resources", "v2", "jaffle_shop", "manifest.json"))
        with open(path, "r") as fp:
            self.manifest_v2_json = json.load(fp)
        self.manifest_v2_obj = manifest.Manifest(**self.manifest_v2_json)

    def test_to_bigquery_schema(self):
        value = manifest.Manifest.to_bigquery_schema()
        with open("/tmp/foo.json", "w") as fp:
            data = [x.to_api_repr() for x in value]
            json.dump(data, fp)
        self.assertEqual(len(value), 10)

    def test_get_classs_name(self):
        self.assertEqual(self.manifest_v2_obj.__class__.get_class_name(), "Manifest")

    def test_get_fields(self):
        self.assertEqual(len(self.manifest_v2_obj.__class__.get_fields()), 10)

    def test_get_field(self):
        nodes = self.manifest_v2_obj.__class__.get_field("nodes")
        self.assertEqual(nodes.name, "nodes")

    def test_to_dict(self):
        manifest_obj = manifest.Manifest(**self.manifest_v2_json)
        manifest_obj_dict = manifest_obj.to_dict(depth=0)
        expected = ['metadata', 'nodes', 'sources', 'macros', 'docs', 'exposures',
                    'selectors', 'disabled', 'parent_map', 'child_map']
        self.assertListEqual(list(manifest_obj_dict.keys()), expected)
        self.assertDictEqual(manifest_obj.metadata.to_dict(depth=0),
                             {
                                 'adapter_type': 'bigquery',
                                 'dbt_schema_version': 'https://schemas.getdbt.com/dbt/manifest/v1.json',
                                 'dbt_version': '0.19.1',
                                 'env': [],
                                 'generated_at': '2021-08-12T09:11:53',
                                 'invocation_id': '196871b6-901c-4992-9c1e-10f8a44b999f',
                                 'project_id': '06e5b98c2db46f8a72cc4f66410e9b3b',
                                 'send_anonymous_usage_stats': False,
                                 'user_id': None
                             })

        # [x.pop("value", None) for x in value["nodes"]]

        # bigquery_client = bigquery.Client(project="ubie-yu-sandbox")
        # full_destination_table_id = "{}.{}.{}".format(
        #     "ubie-yu-sandbox", "test_in_tokyo", "test_table")
        # statuses = bigquery_client.insert_rows_json(
        #     table=full_destination_table_id, json_rows=[value], ignore_unknown_values=True)
        # pprint(statuses)
        # self.assertDictEqual(manifest_obj.__dict__, {})
