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
from enum import Enum
from typing import Type

from dbt_artifacts_loader.dbt.base_bigquery_model import BaseBigQueryModel
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
# v7
from dbt_artifacts_loader.dbt.v7.manifest import ManifestV7
# v8
from dbt_artifacts_loader.dbt.v8.manifest import ManifestV8
from dbt_artifacts_loader.dbt.v9.manifest import ManifestV9


class DestinationTables(Enum):
    """Destination tables"""
    # V1
    CATALOG_V1 = "catalog_v1"
    MANIFEST_V1 = "manifest_v1"
    RUN_RESULTS_V1 = "run_results_v1"
    SOURCES_V1 = "sources_v1"
    # V2
    MANIFEST_V2 = "manifest_v2"
    RUN_RESULTS_V2 = "run_results_v2"
    SOURCES_V2 = "sources_v2"
    # V3
    MANIFEST_V3 = "manifest_v3"
    RUN_RESULTS_V3 = "run_results_v3"
    SOURCES_V3 = "sources_v3"
    # V4
    MANIFEST_V4 = "manifest_v4"
    RUN_RESULTS_V4 = "run_results_v4"
    # V5
    MANIFEST_V5 = "manifest_v5"
    # V6
    MANIFEST_V6 = "manifest_v6"
    # V7
    MANIFEST_V7 = "manifest_v7"
    # V8
    MANIFEST_V8 = "manifest_v8"
    # V9
    MANIFEST_V9 = "manifest_v9"


class ArtifactsTypes(Enum):
    """Dbt artifacts types"""
    # V1
    CATALOG_V1 = "CatalogV1"
    MANIFEST_V1 = "ManifestV1"
    RUN_RESULTS_V1 = "RunResultsV1"
    SOURCES_V1 = "SourcesV1"
    # V2
    MANIFEST_V2 = "ManifestV2"
    RUN_RESULTS_V2 = "RunResultsV2"
    SOURCES_V2 = "SourcesV2"
    # V3
    MANIFEST_V3 = "ManifestV3"
    RUN_RESULTS_V3 = "RunResultsV3"
    SOURCES_V3 = "SourcesV3"
    # V4
    MANIFEST_V4 = "ManifestV4"
    RUN_RESULTS_V4 = "RunResultsV4"
    # V5
    MANIFEST_V5 = "ManifestV5"
    # V6
    MANIFEST_V6 = "ManifestV6"
    # V7
    MANIFEST_V7 = "ManifestV7"
    # V8
    MANIFEST_V8 = "ManifestV8"
    # V9
    MANIFEST_V9 = "ManifestV9"


@dataclass
class ArtifactInfo:
    dbt_schema_version: str
    artifact_type: ArtifactsTypes
    destination_table: DestinationTables
    model_class: Type[BaseBigQueryModel]


ARTIFACT_INFO = {
    # V1
    "CATALOG_V1": ArtifactInfo("https://schemas.getdbt.com/dbt/catalog/v1.json",
                               ArtifactsTypes.CATALOG_V1, DestinationTables.CATALOG_V1, CatalogV1),
    "MANIFEST_V1": ArtifactInfo("https://schemas.getdbt.com/dbt/manifest/v1.json",
                                ArtifactsTypes.MANIFEST_V1, DestinationTables.MANIFEST_V1, ManifestV1),
    "RUN_RESULTS_V1": ArtifactInfo("https://schemas.getdbt.com/dbt/run-results/v1.json",
                                   ArtifactsTypes.RUN_RESULTS_V1, DestinationTables.RUN_RESULTS_V1, RunResultsV1),
    "SOURCES_V1": ArtifactInfo("https://schemas.getdbt.com/dbt/sources/v1.json",
                               ArtifactsTypes.SOURCES_V1, DestinationTables.SOURCES_V1, SourcesV1),
    # V2
    "MANIFEST_V2": ArtifactInfo("https://schemas.getdbt.com/dbt/manifest/v2.json",
                                ArtifactsTypes.MANIFEST_V2, DestinationTables.MANIFEST_V2, ManifestV2),
    "RUN_RESULTS_V2": ArtifactInfo("https://schemas.getdbt.com/dbt/run-results/v2.json",
                                   ArtifactsTypes.RUN_RESULTS_V2, DestinationTables.RUN_RESULTS_V2, RunResultsV2),
    "SOURCES_V2": ArtifactInfo("https://schemas.getdbt.com/dbt/sources/v2.json",
                               ArtifactsTypes.SOURCES_V2, DestinationTables.SOURCES_V2, SourcesV2),
    # V3
    "MANIFEST_V3": ArtifactInfo("https://schemas.getdbt.com/dbt/manifest/v3.json",
                                ArtifactsTypes.MANIFEST_V3, DestinationTables.MANIFEST_V3, ManifestV3),
    "RUN_RESULTS_V3": ArtifactInfo("https://schemas.getdbt.com/dbt/run-results/v3.json",
                                   ArtifactsTypes.RUN_RESULTS_V3, DestinationTables.RUN_RESULTS_V3, RunResultsV3),
    "SOURCES_V3": ArtifactInfo("https://schemas.getdbt.com/dbt/sources/v3.json",
                               ArtifactsTypes.SOURCES_V3, DestinationTables.SOURCES_V3, SourcesV3),
    # V4
    "MANIFEST_V4": ArtifactInfo("https://schemas.getdbt.com/dbt/manifest/v4.json",
                                ArtifactsTypes.MANIFEST_V4, DestinationTables.MANIFEST_V4, ManifestV4),
    "RUN_RESULTS_V4": ArtifactInfo("https://schemas.getdbt.com/dbt/run-results/v4.json",
                                   ArtifactsTypes.RUN_RESULTS_V4, DestinationTables.RUN_RESULTS_V4, RunResultsV4),
    # V5
    "MANIFEST_V5": ArtifactInfo("https://schemas.getdbt.com/dbt/manifest/v5.json",
                                ArtifactsTypes.MANIFEST_V5, DestinationTables.MANIFEST_V5, ManifestV5),
    # V6
    "MANIFEST_V6": ArtifactInfo("https://schemas.getdbt.com/dbt/manifest/v6.json",
                                ArtifactsTypes.MANIFEST_V6, DestinationTables.MANIFEST_V6, ManifestV6),
    # V7
    "MANIFEST_V7": ArtifactInfo("https://schemas.getdbt.com/dbt/manifest/v7.json",
                                ArtifactsTypes.MANIFEST_V7, DestinationTables.MANIFEST_V7, ManifestV7),
    # V8
    "MANIFEST_V8": ArtifactInfo("https://schemas.getdbt.com/dbt/manifest/v8.json",
                                ArtifactsTypes.MANIFEST_V8, DestinationTables.MANIFEST_V8, ManifestV8),
    # V9
    "MANIFEST_V9": ArtifactInfo("https://schemas.getdbt.com/dbt/manifest/v9.json",
                                ArtifactsTypes.MANIFEST_V9, DestinationTables.MANIFEST_V9, ManifestV9),
}
