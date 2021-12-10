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
from enum import Enum
import datetime
from datetime import date, datetime
from typing import Optional, List
from dataclasses import dataclass

from google.cloud import bigquery


class DestinationTables(Enum):
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


class ArtifactsTypes(Enum):
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


@dataclass
class ArtifactInfo:
    dbt_schema_version: str
    artifact_type: ArtifactsTypes
    destination_table: DestinationTables


ARTIFACT_INFO = {
    # V1
    "CATALOG_V1": ArtifactInfo("https://schemas.getdbt.com/dbt/catalog/v1.json",
                               ArtifactsTypes.CATALOG_V1, DestinationTables.CATALOG_V1),
    "MANIFEST_V1": ArtifactInfo("https://schemas.getdbt.com/dbt/manifest/v1.json",
                                ArtifactsTypes.MANIFEST_V1, DestinationTables.MANIFEST_V1),
    "RUN_RESULTS_V1": ArtifactInfo("https://schemas.getdbt.com/dbt/run-results/v1.json",
                                   ArtifactsTypes.RUN_RESULTS_V1, DestinationTables.RUN_RESULTS_V1),
    "SOURCES_V1": ArtifactInfo("https://schemas.getdbt.com/dbt/sources/v1.json",
                               ArtifactsTypes.SOURCES_V1, DestinationTables.SOURCES_V1),
    # V2
    "MANIFEST_V2": ArtifactInfo("https://schemas.getdbt.com/dbt/manifest/v2.json",
                                ArtifactsTypes.MANIFEST_V2, DestinationTables.MANIFEST_V2),
    "RUN_RESULTS_V2": ArtifactInfo("https://schemas.getdbt.com/dbt/run-results/v2.json",
                                   ArtifactsTypes.RUN_RESULTS_V2, DestinationTables.RUN_RESULTS_V2),
    "SOURCES_V2": ArtifactInfo("https://schemas.getdbt.com/dbt/sources/v2.json",
                               ArtifactsTypes.SOURCES_V2, DestinationTables.SOURCES_V2),
    # V3
    "MANIFEST_V3": ArtifactInfo("https://schemas.getdbt.com/dbt/manifest/v3.json",
                                ArtifactsTypes.MANIFEST_V3, DestinationTables.MANIFEST_V3),
    "RUN_RESULTS_V3": ArtifactInfo("https://schemas.getdbt.com/dbt/run-results/v3.json",
                                   ArtifactsTypes.RUN_RESULTS_V3, DestinationTables.RUN_RESULTS_V3),
    "SOURCES_V3": ArtifactInfo("https://schemas.getdbt.com/dbt/sources/v3.json",
                               ArtifactsTypes.SOURCES_V3, DestinationTables.SOURCES_V3),
    # V4
    "MANIFEST_V4": ArtifactInfo("https://schemas.getdbt.com/dbt/manifest/v4.json",
                                ArtifactsTypes.MANIFEST_V4, DestinationTables.MANIFEST_V4),
    "RUN_RESULTS_V4": ArtifactInfo("https://schemas.getdbt.com/dbt/run-results/v4.json",
                                   ArtifactsTypes.RUN_RESULTS_V4, DestinationTables.RUN_RESULTS_V4),
}


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


def get_artifact_type_by_id(dbt_schema_version: str) -> Optional["ArtifactsTypes"]:
    """Get one of the enumeration values by the schema ID

    Args:
        dbt_schema_version (str): The schema ID

    Returns:
        one of ArtifactsTypeV1 values
    """
    for _, artifact_info in ARTIFACT_INFO.items():
        if dbt_schema_version == artifact_info.dbt_schema_version:
            return artifact_info.artifact_type
    return None


def get_destination_table(artifact_type: ArtifactsTypes) -> Optional[DestinationTables]:
    """Get the destination table

    Args:
        artifact_type:

    Returns:
        (str) the destination BigQuery table ID
    """
    for _, artifact_info in ARTIFACT_INFO.items():
        if artifact_type == artifact_info.artifact_type:
            return artifact_info.destination_table
    return None


def get_default_load_job_config(schema: List[bigquery.SchemaField]) -> bigquery.LoadJobConfig:
    """Get the default load job config"""
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND
    job_config.schema = schema
    return job_config


def load_table_from_json(
        client: bigquery.Client,
        job_config: bigquery.LoadJobConfig,
        table: str,
        json_rows: list):
    """Load JSON rows INTO the destination table"""
    job = client.load_table_from_json(destination=table,
                                      json_rows=json_rows,
                                      job_config=job_config)
    try:
        result = job.result()
        return result
    # TODO handle the exception in details.
    # pylint: disable=W0703
    except Exception as e:
        raise RuntimeError(job.errors) from e
