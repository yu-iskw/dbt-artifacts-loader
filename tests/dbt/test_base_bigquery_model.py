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
# v1
from dbt_artifacts_loader.dbt.v1.catalog import CatalogV1
from dbt_artifacts_loader.dbt.v1.manifest import ManifestV1
from dbt_artifacts_loader.dbt.v1.run_results import RunResultsV1
from dbt_artifacts_loader.dbt.v1.sources import SourcesV1
# v2
from dbt_artifacts_loader.dbt.v2.manifest import ManifestV2
from dbt_artifacts_loader.dbt.v2.run_results import RunResultsV2

from dbt_artifacts_loader.utils import get_project_root


def load_artifact_json(version: str, json_file: str) -> dict:
    path = os.path.abspath(
        os.path.join(get_project_root(), "tests", "resources", version, "jaffle_shop", json_file))
    with open(path, "r") as fp:
        return json.load(fp)


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
        # v1
        self.catalog_v1_obj = CatalogV1(**(load_artifact_json("v1", "catalog.json")))
        self.manifest_v1_obj = ManifestV1(**(load_artifact_json("v1", "manifest.json")))
        self.run_results_v1_obj = RunResultsV1(**(load_artifact_json("v1", "run_results.json")))
        # v2
        self.manifest_v2_obj = ManifestV2(**(load_artifact_json("v2", "manifest.json")))
        self.run_results_v2_obj = RunResultsV2(**(load_artifact_json("v2", "run_results.json")))

    def test_to_bigquery_schema(self):
        value = ManifestV1.to_bigquery_schema()
        self.assertEqual(len(value), 10)

    def test_get_classs_name(self):
        self.assertEqual(self.manifest_v2_obj.__class__.get_class_name(), "ManifestV2")

    def test_get_fields(self):
        self.assertEqual(len(self.manifest_v2_obj.__class__.get_fields()), 10)

    def test_get_field(self):
        nodes = self.manifest_v2_obj.__class__.get_field("nodes")
        self.assertEqual(nodes.name, "nodes")

    def test_to_dict_for_artifacts_v1(self):
        artifact_dict = self.catalog_v1_obj.to_dict(depth=0)
        self.assertEqual(len(artifact_dict.keys()), 4)
        artifact_dict = self.manifest_v1_obj.to_dict(depth=0)
        self.assertEqual(len(artifact_dict.keys()), 10)
        artifact_dict = self.run_results_v1_obj.to_dict(depth=0)
        self.assertEqual(len(artifact_dict.keys()), 4)

    def test_to_dict_for_artifacts_v2(self):
        artifact_dict = self.manifest_v2_obj.to_dict(depth=0)
        self.assertEqual(len(artifact_dict.keys()), 10)
        artifact_dict = self.run_results_v2_obj.to_dict(depth=0)
        self.assertEqual(len(artifact_dict.keys()), 4)

    def test_to_dict(self):
        manifest_obj_dict = self.manifest_v2_obj.to_dict(depth=0)
        expected = ['metadata', 'nodes', 'sources', 'macros', 'docs', 'exposures',
                    'selectors', 'disabled', 'parent_map', 'child_map']
        self.assertListEqual(list(manifest_obj_dict.keys()), expected)
        self.assertDictEqual(self.manifest_v2_obj.metadata.to_dict(depth=0),
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
