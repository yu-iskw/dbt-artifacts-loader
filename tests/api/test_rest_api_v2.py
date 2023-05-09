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
import json
import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from dbt_artifacts_loader.api import rest_api_v2
from dbt_artifacts_loader.utils import get_project_root


def get_mock_value_of_download_gcs_object_as_text():
    """Mock download_gcs_object_as_text"""
    path = os.path.join(get_project_root(), "tests", "resources", "v2", "jaffle_shop", "run_results.json")
    with open(path, "r", encoding="utf-8") as fp:
        return fp.read()


class TestRestAPI(unittest.TestCase):

    def test_healthcheck(self):
        client = TestClient(rest_api_v2.app)
        response = client.get("/healthcheck")
        assert response.status_code == 200
        assert response.json() == {'status': 'ok', "test_mode": True}

    # NOTE Please be careful on how to import download_gcs_object_as_text in the module.
    @patch("dbt_artifacts_loader.api.rest_api_v2.download_gcs_object_as_text")
    def test_insert_artifact_v2(self, mock_download_gcs_object_as_text):
        mock_download_gcs_object_as_text.return_value = get_mock_value_of_download_gcs_object_as_text()

        # Get the testing request body
        path = os.path.join(get_project_root(), "tests", "resources", "pubsub", "test_message.json")
        with open(path, "r", encoding="utf-8") as fp:
            request_body = json.load(fp)
        # Test request
        client = TestClient(rest_api_v2.app)
        response = client.post("/api/v2/", json=request_body)
        assert response.json() == {
            'source_uri': 'gs://your-gcp-project-dbt-artifacts/test/run_results.json',
            'table_id': 'test-destination-project.test_dataset.run_results_v2',
            'statuses': [],
            "test_mode": True,
        }
        assert response.status_code == 200
