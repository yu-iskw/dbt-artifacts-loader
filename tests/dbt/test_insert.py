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

from google.cloud import bigquery

# v1
from dbt_artifacts_loader.dbt.v1.catalog import CatalogV1
from dbt_artifacts_loader.dbt.v1.manifest import ManifestV1
from dbt_artifacts_loader.dbt.v1.run_results import RunResultsV1
# v2
from dbt_artifacts_loader.dbt.v2.manifest import ManifestV2
from dbt_artifacts_loader.dbt.v2.run_results import RunResultsV2

from dbt_artifacts_loader.utils import get_project_root


def load_artifact_json(version: str, json_file: str) -> dict:
    path = os.path.abspath(
        os.path.join(get_project_root(), "tests", "resources", version, "jaffle_shop", json_file))
    with open(path, "r", encoding="utf-8") as fp:
        return json.load(fp)


class TestInsert(unittest.TestCase):

    def setUp(self):
        # v1
        self.catalog_v1_obj = CatalogV1(**(load_artifact_json("v1", "catalog.json")))
        self.manifest_v1_obj = ManifestV1(**(load_artifact_json("v1", "manifest.json")))
        self.run_results_v1_obj = RunResultsV1(**(load_artifact_json("v1", "run_results.json")))
        # v2
        self.manifest_v2_obj = ManifestV2(**(load_artifact_json("v2", "manifest.json")))
        self.run_results_v2_obj = RunResultsV2(**(load_artifact_json("v2", "run_results.json")))

    @unittest.SkipTest
    def test_insert(self):
        project_id = "YOUR-GCP-PROJECT"
        client = bigquery.Client(project=project_id)
        # catalog_v1
        table = f"{project_id}.dbt_artifacts.catalog_v1"
        status = client.insert_rows_json(table=table,
                                         json_rows=[self.catalog_v1_obj.to_dict(depth=0)],
                                         ignore_unknown_values=True)
        self.assertListEqual(status, [])
        # manifest_v1
        table = f"{project_id}.dbt_artifacts.manifest_v1"
        status = client.insert_rows_json(table=table,
                                         json_rows=[self.manifest_v1_obj.to_dict(depth=0)],
                                         ignore_unknown_values=True)
        self.assertListEqual(status, [])
        # run_results_v1
        table = f"{project_id}.dbt_artifacts.run_results_v1"
        status = client.insert_rows_json(table=table,
                                         json_rows=[self.run_results_v1_obj.to_dict(depth=0)],
                                         ignore_unknown_values=True)
        self.assertListEqual(status, [])
        # manifest_v2
        table = f"{project_id}.dbt_artifacts.manifest_v2"
        status = client.insert_rows_json(table=table,
                                         json_rows=[self.manifest_v2_obj.to_dict(depth=0)],
                                         ignore_unknown_values=True)
        self.assertListEqual(status, [])
        # run_results_v2
        table = f"{project_id}.dbt_artifacts.run_results_v2"
        status = client.insert_rows_json(table=table,
                                         json_rows=[self.run_results_v2_obj.to_dict(depth=0)],
                                         ignore_unknown_values=True)
        self.assertListEqual(status, [])
