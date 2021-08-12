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
import base64
import json
from functools import lru_cache
from typing import Optional, Union, List
import datetime

from fastapi import FastAPI, Depends, HTTPException
# pylint: disable=E0611
from pydantic import BaseModel
from pydantic import Field

from google.cloud import bigquery

from dbt_artifacts_loader.utils import download_gcs_object_as_text
from dbt_artifacts_loader.api import config
from dbt_artifacts_loader.dbt.utils import get_dbt_schema_version
from dbt_artifacts_loader.dbt.utils import ArtifactsTypes, DestinationTables

app = FastAPI()


# pylint: disable=C0103
class MessageBody(BaseModel):
    """Pub/Sub message"""
    attributes: Optional[dict]
    data: str
    messageId: str
    message_id: str
    publishTime: datetime.datetime
    publish_time: datetime.datetime


# pylint: disable=C0103
class RequestBody(BaseModel):
    """Request body for GCS notifications from Cloud Pub/Sub"""
    message: MessageBody
    subscription: str


class Response(BaseModel):
    source_uri: Union[str, List[str]] = Field(description="source URI(s)")
    table_id: str = Field(description="table path")
    statuses: Optional[List[dict]] = Field(description="Insert results", default=[])
    test_mode: Optional[bool] = Field(description="test mode or not", default=False)


@lru_cache()
def get_settings() -> config.APISettings:
    """Get API settings"""
    return config.APISettings()


@app.get("/healthcheck")
def healthcheck(settings: config.APISettings = Depends(get_settings)):
    """Health check endpoint"""
    test_mode = settings.test_mode
    response = {"status": "ok"}
    if test_mode is True:
        response["test_mode"] = True
    return response


@app.post("/api/v1/")
def insert_artifact_v1(request_body: RequestBody, settings: config.APISettings = Depends(get_settings)):
    """Insert a JSON file of dbt artifacts v1.

    NOTE:
        The base configuration is implemented in `config.py`.
        We can pass concrete values to it with an `.env.xxx` file.
        The fixed `.env.xxx` are located in the `.env/` directory.

    Args:
        request_body (RequestBody): request body
        settings: application settings
    """
    # Collect settings
    client_project = settings.client_project
    destination_project = settings.destination_project
    destination_dataset = settings.destination_dataset
    test_mode = settings.test_mode

    # Get the requested data.
    print(request_body.json())
    data = json.loads(base64.b64decode(request_body.message.data).decode("utf-8").strip())
    print(data)

    # Download/read a JSON file from GCS
    bucket = data["bucket"]
    name = data["name"]

    if data["contentType"] != "application/json":
        return {"message": "gs://{}/{} is not application/json".format(bucket, name)}

    try:
        print("Download gs://{}/{}".format(bucket, name))
        artifact_json_text = download_gcs_object_as_text(project=client_project, bucket=bucket, name=name)
        print("artifact_json_text: {}".format(artifact_json_text))
        artifact_json = json.loads(artifact_json_text)
    except Exception as e:
        detail = "Can not download the GCS object gs://{}/{}: {}".format(bucket, name, str(e))
        raise HTTPException(status_code=500, detail=detail) from e

    # Check if the JSON file is one of dbt artifacts types.
    dbt_schema_version = get_dbt_schema_version(artifact_json=artifact_json)
    artifact_type = ArtifactsTypes.get_artifact_type_by_id(dbt_schema_version=dbt_schema_version)
    # TODO support catalog.json and manifest.json
    available_artifact_types = [
        ArtifactsTypes.RUN_RESULTS_V1, ArtifactsTypes.SOURCES_V1,
        ArtifactsTypes.RUN_RESULTS_V2,
    ]
    if artifact_type not in available_artifact_types:
        return {"message": "gs://{}/{} is not a dbt artifact or is not supported".format(bucket, name)}

    # Insert a dbt artifact JSON
    destination_table_id = DestinationTables.get_destination_table(artifact_type=artifact_type)

    full_destination_table_id = "{}.{}.{}".format(
        destination_project, destination_dataset, destination_table_id.value)
    statuses = []
    print("Insert into {}".format(full_destination_table_id))
    if test_mode is False:
        try:
            bigquery_client = bigquery.Client(project=client_project)
            print(artifact_json)
            statuses = bigquery_client.insert_rows_json(
                table=full_destination_table_id, json_rows=[artifact_json], ignore_unknown_values=True)
        except Exception as e:
            # TODO fix the logger
            # logger.error({"message": str(e)})
            detail = "Can not insert artifact to {}: {}".format(full_destination_table_id, str(e))
            raise HTTPException(status_code=500, detail=detail) from e

    # Construct a response
    response = Response.construct(
        source_uri="gs://{}/{}".format(bucket, name),
        table_id=full_destination_table_id,
        statuses=statuses,
        test_mode=test_mode,
    )
    return response
