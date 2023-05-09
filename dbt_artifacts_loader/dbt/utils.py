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
from typing import List, Optional, Type

from google.cloud import bigquery

from dbt_artifacts_loader.dbt.base_bigquery_model import BaseBigQueryModel
from dbt_artifacts_loader.dbt.version_map import (ARTIFACT_INFO,
                                                  ArtifactsTypes,
                                                  DestinationTables)


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


def get_model_class(artifact_type: ArtifactsTypes) -> Type[BaseBigQueryModel]:
    """Get the model class

    Args:
        artifact_type (ArtifactsTypes): artifact type

    Returns:
        the model class
    """
    # v1
    for _, artifact_info in ARTIFACT_INFO.items():
        if artifact_type == artifact_info.artifact_type:
            return artifact_info.model_class
    raise ValueError(f"No such an artifact {artifact_type}")
