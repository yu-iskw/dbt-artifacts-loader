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

from dbt_artifacts_loader.dbt.utils import ArtifactsTypes
from dbt_artifacts_loader.dbt.v1.catalog import CatalogV1
from dbt_artifacts_loader.dbt.v1.manifest import ManifestV1
from dbt_artifacts_loader.dbt.v1.run_results import RunResultsV1
from dbt_artifacts_loader.dbt.v1.sources import SourcesV1
from dbt_artifacts_loader.dbt.v2.manifest import ManifestV2
from dbt_artifacts_loader.dbt.v2.run_results import RunResultsV2
from dbt_artifacts_loader.dbt.model_factory import get_model_class


class TestModelFactory(unittest.TestCase):

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
        ]
        for (artifact_type, expected_class) in test_sets:
            klass = get_model_class(artifact_type=artifact_type)
            self.assertEqual(klass, expected_class)
