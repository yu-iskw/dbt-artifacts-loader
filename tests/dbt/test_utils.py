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


from dbt_artifacts_loader.utils import get_project_root
from dbt_artifacts_loader.dbt.utils import get_dbt_schema_version


class TestDbtUtils(unittest.TestCase):

    def test_get_dbt_schema_version(self):
        # v1
        v1_artifacts = {
            "catalog.json": "https://schemas.getdbt.com/dbt/catalog/v1.json",
            "manifest.json": "https://schemas.getdbt.com/dbt/manifest/v1.json",
            "run_results.json": "https://schemas.getdbt.com/dbt/run-results/v1.json",
        }
        for file, expected_dbt_schema_version in v1_artifacts.items():
            path = os.path.join(get_project_root(), "tests", "resources", "v1", "jaffle_shop", file)
            with open(path, "r", encoding="utf-8") as fp:
                artifact_json = json.load(fp)
                dbt_schema_version = get_dbt_schema_version(artifact_json=artifact_json)
                self.assertEqual(dbt_schema_version, expected_dbt_schema_version)
        # v2
        v1_artifacts = {
            "manifest.json": "https://schemas.getdbt.com/dbt/manifest/v2.json",
            "run_results.json": "https://schemas.getdbt.com/dbt/run-results/v2.json",
        }
        for file, expected_dbt_schema_version in v1_artifacts.items():
            path = os.path.join(get_project_root(), "tests", "resources", "v2", "jaffle_shop", file)
            with open(path, "r", encoding="utf-8") as fp:
                artifact_json = json.load(fp)
                dbt_schema_version = get_dbt_schema_version(artifact_json=artifact_json)
                self.assertEqual(dbt_schema_version, expected_dbt_schema_version)
        # v3
        v1_artifacts = {
            "manifest.json": "https://schemas.getdbt.com/dbt/manifest/v3.json",
            "run_results.json": "https://schemas.getdbt.com/dbt/run-results/v3.json",
        }
        for file, expected_dbt_schema_version in v1_artifacts.items():
            path = os.path.join(get_project_root(), "tests", "resources", "v3", "jaffle_shop", file)
            with open(path, "r", encoding="utf-8") as fp:
                artifact_json = json.load(fp)
                dbt_schema_version = get_dbt_schema_version(artifact_json=artifact_json)
                self.assertEqual(dbt_schema_version, expected_dbt_schema_version)
