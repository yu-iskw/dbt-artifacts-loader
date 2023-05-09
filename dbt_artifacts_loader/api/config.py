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

from pydantic import BaseSettings
from setuptools._distutils.util import strtobool


def get_env_file() -> str:
    """Get an environment-specific '.env' file

    Returns:
        str: .env file name
    """
    # TODO choose the env file.
    environment = os.getenv('ENV_FILE', '.env/.env.test')
    return environment


class APISettings(BaseSettings):
    """Settings for Fast API"""
    # GCP project ID for BigQuery client
    client_project: str = None
    # Destination BigQuery project ID
    destination_project: str = os.getenv("DESTINATION_PROJECT", None)
    # Destination BigQuery dataset ID
    destination_dataset: str = os.getenv("DESTINATION_DATASET", None)
    # Run as the dry run mode if true
    test_mode: bool = bool(strtobool(os.getenv("TEST_MODE", "False")))

    class Config:
        env_file = get_env_file()
