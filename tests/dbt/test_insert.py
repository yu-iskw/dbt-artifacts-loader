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
from dbt_artifacts_loader.dbt.utils import get_default_load_job_config, load_table_from_json
from dbt_artifacts_loader.dbt.v1.catalog import CatalogV1
from dbt_artifacts_loader.dbt.v1.manifest import ManifestV1
from dbt_artifacts_loader.dbt.v1.run_results import RunResultsV1
from dbt_artifacts_loader.dbt.v2.manifest import ManifestV2
from dbt_artifacts_loader.dbt.v2.run_results import RunResultsV2
from dbt_artifacts_loader.dbt.v3.manifest import ManifestV3
from dbt_artifacts_loader.dbt.v3.run_results import RunResultsV3
from dbt_artifacts_loader.dbt.v4.manifest import ManifestV4
from dbt_artifacts_loader.dbt.v4.run_results import RunResultsV4

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
        # v3
        self.manifest_v3_obj = ManifestV3(**(load_artifact_json("v3", "manifest.json")))
        self.run_results_v3_obj = RunResultsV3(**(load_artifact_json("v3", "run_results.json")))
        # v4
        self.manifest_v4_obj = ManifestV4(**(load_artifact_json("v4", "manifest.json")))
        self.run_results_v4_obj = RunResultsV4(**(load_artifact_json("v4", "run_results.json")))

    @unittest.SkipTest
    def test_insert(self):
        project_id = "YOUR-GCP-PROJECT"
        client = bigquery.Client(project=project_id)
        # catalog_v1
        table = f"{project_id}.dbt_artifacts.catalog_v1"
        schema = self.catalog_v1_obj.__class__.to_bigquery_schema(depth=0)
        job_config = get_default_load_job_config(schema=schema)
        job_result = load_table_from_json(client=client,
                                          table=table,
                                          json_rows=[self.catalog_v1_obj.to_dict(depth=0)],
                                          job_config=job_config)
        self.assertEqual(job_result.errors, None)
        # manifest_v1
        table = f"{project_id}.dbt_artifacts.manifest_v1"
        schema = self.manifest_v1_obj.__class__.to_bigquery_schema(depth=0)
        job_config = get_default_load_job_config(schema=schema)
        job_result = load_table_from_json(client=client,
                                          table=table,
                                          json_rows=[self.manifest_v1_obj.to_dict(depth=0)],
                                          job_config=job_config)
        self.assertEqual(job_result.errors, None)
        # run_results_v1
        table = f"{project_id}.dbt_artifacts.run_results_v1"
        schema = self.run_results_v1_obj.__class__.to_bigquery_schema(depth=0)
        job_config = get_default_load_job_config(schema=schema)
        job_result = load_table_from_json(client=client,
                                          table=table,
                                          json_rows=[self.run_results_v1_obj.to_dict(depth=0)],
                                          job_config=job_config)
        self.assertEqual(job_result.errors, None)
        # manifest_v2
        table = f"{project_id}.dbt_artifacts.manifest_v2"
        schema = self.manifest_v2_obj.__class__.to_bigquery_schema(depth=0)
        job_config = get_default_load_job_config(schema=schema)
        job_result = load_table_from_json(client=client,
                                          table=table,
                                          json_rows=[self.manifest_v2_obj.to_dict(depth=0)],
                                          job_config=job_config)
        self.assertEqual(job_result.errors, None)
        # run_results_v2
        table = f"{project_id}.dbt_artifacts.run_results_v2"
        schema = self.run_results_v2_obj.__class__.to_bigquery_schema(depth=0)
        job_config = get_default_load_job_config(schema=schema)
        job_result = load_table_from_json(client=client,
                                          table=table,
                                          json_rows=[self.run_results_v2_obj.to_dict(depth=0)],
                                          job_config=job_config)
        self.assertEqual(job_result.errors, None)
        # manifest_v3
        table = f"{project_id}.dbt_artifacts.manifest_v3"
        schema = self.manifest_v3_obj.__class__.to_bigquery_schema(depth=0)
        job_config = get_default_load_job_config(schema=schema)
        job_result = load_table_from_json(client=client,
                                          table=table,
                                          json_rows=[self.manifest_v3_obj.to_dict(depth=0)],
                                          job_config=job_config)
        self.assertEqual(job_result.errors, None)
        # run_results_v3
        table = f"{project_id}.dbt_artifacts.run_results_v3"
        schema = self.run_results_v3_obj.__class__.to_bigquery_schema(depth=0)
        job_config = get_default_load_job_config(schema=schema)
        job_result = load_table_from_json(client=client,
                                          table=table,
                                          json_rows=[self.run_results_v3_obj.to_dict(depth=0)],
                                          job_config=job_config)
        self.assertEqual(job_result.errors, None)
        # manifest_v4
        table = f"{project_id}.dbt_artifacts.manifest_v4"
        schema = self.manifest_v4_obj.__class__.to_bigquery_schema(depth=0)
        job_config = get_default_load_job_config(schema=schema)
        job_result = load_table_from_json(client=client,
                                          table=table,
                                          json_rows=[self.manifest_v4_obj.to_dict(depth=0)],
                                          job_config=job_config)
        self.assertEqual(job_result.errors, None)
        # run_results_v4
        table = f"{project_id}.dbt_artifacts.run_results_v4"
        schema = self.run_results_v4_obj.__class__.to_bigquery_schema(depth=0)
        job_config = get_default_load_job_config(schema=schema)
        job_result = load_table_from_json(client=client,
                                          table=table,
                                          json_rows=[self.run_results_v4_obj.to_dict(depth=0)],
                                          job_config=job_config)
        self.assertEqual(job_result.errors, None)
