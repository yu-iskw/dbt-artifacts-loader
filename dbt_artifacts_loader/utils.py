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

from google.cloud import storage


def get_project_root() -> str:
    """Get the path to the project root.

    Returns:
        str: the path to the project root.
    """
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def get_module_root() -> str:
    """Get the path to the module root.

    Returns:
        str: the path to the module root.
    """
    return os.path.abspath(os.path.dirname(__file__))


def download_gcs_object_as_text(project: str, bucket: str, name: str):
    """Download the GCS object as text

    Args:
        project (str): the GCP project ID
        bucket (str): the GCS bucket
        name (str): the GCS object name

    Returns:
        (str) the content of the GCS object as text
    """
    try:
        storage_client = storage.Client(project=project)
        bucket = storage_client.get_bucket(bucket_or_name=bucket)
        blob = storage.Blob(name=name, bucket=bucket)
        artifact_json = blob.download_as_text()
        return artifact_json
    # TODO handle the exception appropriately
    # pylint: disable=W0703
    except Exception as e:
        raise RuntimeError from e
    return None
