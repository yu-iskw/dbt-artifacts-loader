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
from dbt_artifacts_loader.dbt.utils import ArtifactsTypes
from dbt_artifacts_loader.dbt.v1.catalog import CatalogV1
from dbt_artifacts_loader.dbt.v1.manifest import ManifestV1
from dbt_artifacts_loader.dbt.v1.run_results import RunResultsV1
from dbt_artifacts_loader.dbt.v1.sources import SourcesV1
from dbt_artifacts_loader.dbt.v2.manifest import ManifestV2
from dbt_artifacts_loader.dbt.v2.run_results import RunResultsV2
from dbt_artifacts_loader.dbt.v2.sources import SourcesV2
from dbt_artifacts_loader.dbt.v3.manifest import ManifestV3
from dbt_artifacts_loader.dbt.v3.run_results import RunResultsV3


def get_model_class(artifact_type: ArtifactsTypes):
    """Get the model class

    Args:
        artifact_type (ArtifactsTypes): artifact type

    Returns:
        the model class
    """
    # v1
    if artifact_type == ArtifactsTypes.CATALOG_V1:
        return CatalogV1
    elif artifact_type == ArtifactsTypes.MANIFEST_V1:
        return ManifestV1
    elif artifact_type == ArtifactsTypes.RUN_RESULTS_V1:
        return RunResultsV1
    elif artifact_type == ArtifactsTypes.SOURCES_V1:
        return SourcesV1
    # v2
    elif artifact_type == ArtifactsTypes.MANIFEST_V2:
        return ManifestV2
    elif artifact_type == ArtifactsTypes.RUN_RESULTS_V2:
        return RunResultsV2
    elif artifact_type == ArtifactsTypes.SOURCES_V2:
        return SourcesV2
    # v3
    elif artifact_type == ArtifactsTypes.MANIFEST_V3:
        return ManifestV3
    elif artifact_type == ArtifactsTypes.RUN_RESULTS_V3:
        return RunResultsV3
    raise ValueError(f"No such an artifact {artifact_type}")
