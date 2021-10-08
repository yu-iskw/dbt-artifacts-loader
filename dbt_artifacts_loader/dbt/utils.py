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
import os.path
from enum import Enum
import datetime
from datetime import date, datetime


def get_project_root():
    """Get the path to the project root

    Returns:
        (str) the path to the project root
    """
    return os.path.abspath(os.path.join(os.path.basedir(__file__), "..", ".."))


def get_module_root():
    """Get the path to the module root

    Returns:
        (str) the path to the module root
    """
    return os.path.abspath(os.path.join(os.path.basedir(__file__), ".."))


def datetime_handler(x):
    """The handler is used to deal with date and datetime"""
    if isinstance(x, (datetime.datetime, datetime.date, datetime, date)):
        return x.isoformat()
    raise TypeError(f'Type {type(x)} not serializable')


def get_dbt_schema_version(artifact_json: dict) -> str:
    """Get the dbt schema version from the dbt artifact JSON

    Args:
        artifact_json (dict): dbt artifacts JSON

    Returns:
        (str): dbt schema version from 'metadata.dbt_schema_version'
    """
    if "metadata" not in artifact_json:
        raise ValueError("'metadata' doesn't exist.")
    if "dbt_schema_version" not in artifact_json["metadata"]:
        raise ValueError("'metadata.dbt_schema_version' doesnt' exist.")
    return artifact_json["metadata"]["dbt_schema_version"]


class ArtifactsTypes(Enum):
    # V1
    CATALOG_V1 = "CatalogV1"
    MANIFEST_V1 = "ManifestV1"
    RUN_RESULTS_V1 = "RunResultsV1"
    SOURCES_V1 = "SourcesV1"
    # V2
    MANIFEST_V2 = "ManifestV2"
    RUN_RESULTS_V2 = "RunResultsV2"

    @classmethod
    def get_artifact_type_by_id(cls, dbt_schema_version: str):
        """Get one of the enumeration values by the schema ID

        Args:
            dbt_schema_version (str): The schema ID

        Returns:
            one of ArtifactsTypeV1 values
        """
        # V1
        if dbt_schema_version == "https://schemas.getdbt.com/dbt/catalog/v1.json":
            return ArtifactsTypes.CATALOG_V1
        elif dbt_schema_version == "https://schemas.getdbt.com/dbt/manifest/v1.json":
            return ArtifactsTypes.MANIFEST_V1
        elif dbt_schema_version == "https://schemas.getdbt.com/dbt/run-results/v1.json":
            return ArtifactsTypes.RUN_RESULTS_V1
        elif dbt_schema_version == "https://schemas.getdbt.com/dbt/sources/v1.json":
            return ArtifactsTypes.SOURCES_V1
        # V2
        elif dbt_schema_version == "https://schemas.getdbt.com/dbt/manifest/v2.json":
            return ArtifactsTypes.MANIFEST_V2
        elif dbt_schema_version == "https://schemas.getdbt.com/dbt/run-results/v2.json":
            return ArtifactsTypes.RUN_RESULTS_V2
        else:
            return None


class DestinationTables(Enum):
    # V1
    CATALOG_V1 = "catalog_v1"
    MANIFEST_V1 = "manifest_v1"
    RUN_RESULTS_V1 = "run_results_v1"
    SOURCES_V1 = "sources_v1"
    # V2
    MANIFEST_V2 = "manifest_v2"
    RUN_RESULTS_V2 = "run_results_v2"

    @classmethod
    def get_destination_table(cls, artifact_type: ArtifactsTypes):
        """Get the destination table

        Args:
            artifact_type:

        Returns:
            (str) the destination BigQuery table ID
        """
        # V1
        if artifact_type == ArtifactsTypes.CATALOG_V1:
            return DestinationTables.CATALOG_V1
        elif artifact_type == ArtifactsTypes.MANIFEST_V1:
            return DestinationTables.MANIFEST_V1
        elif artifact_type == ArtifactsTypes.RUN_RESULTS_V1:
            return DestinationTables.RUN_RESULTS_V1
        elif artifact_type == ArtifactsTypes.SOURCES_V1:
            return DestinationTables.SOURCES_V1
        # V2
        elif artifact_type == ArtifactsTypes.MANIFEST_V2:
            return DestinationTables.MANIFEST_V2
        elif artifact_type == ArtifactsTypes.RUN_RESULTS_V2:
            return DestinationTables.RUN_RESULTS_V2
        else:
            return None
