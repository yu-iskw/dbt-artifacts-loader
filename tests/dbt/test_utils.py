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

# v1
from dbt_artifacts_loader.dbt.v1.catalog import CatalogV1
from dbt_artifacts_loader.dbt.v1.manifest import ManifestV1
from dbt_artifacts_loader.dbt.v1.run_results import RunResultsV1
from dbt_artifacts_loader.dbt.v1.sources import SourcesV1
# v2
from dbt_artifacts_loader.dbt.v2.manifest import ManifestV2
from dbt_artifacts_loader.dbt.v2.run_results import RunResultsV2
from dbt_artifacts_loader.dbt.v2.sources import SourcesV2
# v3
from dbt_artifacts_loader.dbt.v3.manifest import ManifestV3
from dbt_artifacts_loader.dbt.v3.run_results import RunResultsV3
from dbt_artifacts_loader.dbt.v3.sources import SourcesV3
# v4
from dbt_artifacts_loader.dbt.v4.manifest import ManifestV4
from dbt_artifacts_loader.dbt.v4.run_results import RunResultsV4
# v5
from dbt_artifacts_loader.dbt.v5.manifest import ManifestV5
# v6
from dbt_artifacts_loader.dbt.v6.manifest import ManifestV6

from dbt_artifacts_loader.dbt.version_map import ArtifactsTypes
from dbt_artifacts_loader.utils import get_project_root
from dbt_artifacts_loader.dbt.utils import get_dbt_schema_version, get_model_class


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
        v2_artifacts = {
            "manifest.json": "https://schemas.getdbt.com/dbt/manifest/v2.json",
            "run_results.json": "https://schemas.getdbt.com/dbt/run-results/v2.json",
        }
        for file, expected_dbt_schema_version in v2_artifacts.items():
            path = os.path.join(get_project_root(), "tests", "resources", "v2", "jaffle_shop", file)
            with open(path, "r", encoding="utf-8") as fp:
                artifact_json = json.load(fp)
                dbt_schema_version = get_dbt_schema_version(artifact_json=artifact_json)
                self.assertEqual(dbt_schema_version, expected_dbt_schema_version)
        # v3
        v3_artifacts = {
            "manifest.json": "https://schemas.getdbt.com/dbt/manifest/v3.json",
            "run_results.json": "https://schemas.getdbt.com/dbt/run-results/v3.json",
        }
        for file, expected_dbt_schema_version in v3_artifacts.items():
            path = os.path.join(get_project_root(), "tests", "resources", "v3", "jaffle_shop", file)
            with open(path, "r", encoding="utf-8") as fp:
                artifact_json = json.load(fp)
                dbt_schema_version = get_dbt_schema_version(artifact_json=artifact_json)
                self.assertEqual(dbt_schema_version, expected_dbt_schema_version)
        # v4
        v4_artifacts = {
            "manifest.json": "https://schemas.getdbt.com/dbt/manifest/v4.json",
            "run_results.json": "https://schemas.getdbt.com/dbt/run-results/v4.json",
        }
        for file, expected_dbt_schema_version in v4_artifacts.items():
            path = os.path.join(get_project_root(), "tests", "resources", "v4", "jaffle_shop", file)
            with open(path, "r", encoding="utf-8") as fp:
                artifact_json = json.load(fp)
                dbt_schema_version = get_dbt_schema_version(artifact_json=artifact_json)
                self.assertEqual(dbt_schema_version, expected_dbt_schema_version)
        # v5
        v5_artifacts = {
            "manifest.json": "https://schemas.getdbt.com/dbt/manifest/v5.json",
        }
        for file, expected_dbt_schema_version in v5_artifacts.items():
            path = os.path.join(get_project_root(), "tests", "resources", "v5", "jaffle_shop", file)
            with open(path, "r", encoding="utf-8") as fp:
                artifact_json = json.load(fp)
                dbt_schema_version = get_dbt_schema_version(artifact_json=artifact_json)
                self.assertEqual(dbt_schema_version, expected_dbt_schema_version)
        # v6
        v6_artifacts = {
            "manifest.json": "https://schemas.getdbt.com/dbt/manifest/v6.json",
        }
        for file, expected_dbt_schema_version in v6_artifacts.items():
            path = os.path.join(get_project_root(), "tests", "resources", "v6", "jaffle_shop", file)
            with open(path, "r", encoding="utf-8") as fp:
                artifact_json = json.load(fp)
                dbt_schema_version = get_dbt_schema_version(artifact_json=artifact_json)
                self.assertEqual(dbt_schema_version, expected_dbt_schema_version)

    def test_get_model_class(self):
        test_sets = [
            # v1
            (ArtifactsTypes.CATALOG_V1, CatalogV1),
            (ArtifactsTypes.MANIFEST_V1, ManifestV1),
            (ArtifactsTypes.RUN_RESULTS_V1, RunResultsV1),
            (ArtifactsTypes.SOURCES_V1, SourcesV1),
            # v2
            (ArtifactsTypes.MANIFEST_V2, ManifestV2),
            (ArtifactsTypes.RUN_RESULTS_V2, RunResultsV2),
            (ArtifactsTypes.SOURCES_V2, SourcesV2),
            # v3
            (ArtifactsTypes.MANIFEST_V3, ManifestV3),
            (ArtifactsTypes.RUN_RESULTS_V3, RunResultsV3),
            (ArtifactsTypes.SOURCES_V3, SourcesV3),
            # v4
            (ArtifactsTypes.MANIFEST_V4, ManifestV4),
            (ArtifactsTypes.RUN_RESULTS_V4, RunResultsV4),
            # v5
            (ArtifactsTypes.MANIFEST_V5, ManifestV5),
            # v6
            (ArtifactsTypes.MANIFEST_V6, ManifestV6),
        ]
        for (artifact_type, expected_class) in test_sets:
            klass = get_model_class(artifact_type=artifact_type)
            self.assertEqual(klass, expected_class)
