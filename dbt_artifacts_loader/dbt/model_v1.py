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
import json
from dataclasses import dataclass
from enum import Enum

import python_jsonschema_objects as pjs

from dbt_artifacts_loader.utils import get_module_root


class ArtifactsTypesV1(Enum):
    CATALOG = "Catalog"
    MANIFEST = "Manifest"
    RUN_RESULTS = "RunResults"
    SOURCES = "Sources"

    @classmethod
    def get_artifact_type_by_id(cls, schema_id: str):
        """Get one of the enumeration values by the schema ID

        Args:
            schema_id (str): The schema ID

        Returns:
            one of ArtifactsTypeV1 values
        """
        if schema_id == "https://schemas.getdbt.com/dbt/catalog/v1.json":
            return ArtifactsTypesV1.CATALOG
        elif schema_id == "https://schemas.getdbt.com/dbt/manifest/v1.json":
            return ArtifactsTypesV1.MANIFEST
        elif schema_id == "https://schemas.getdbt.com/dbt/run-results/v1.json":
            return ArtifactsTypesV1.RUN_RESULTS
        elif schema_id == "https://schemas.getdbt.com/dbt/sources/v1.json":
            return ArtifactsTypesV1.SOURCES
        else:
            return None


class DestinationTablesV1(Enum):
    CATALOG = "catalog_v1"
    MANIFEST = "manifest_v1"
    RUN_RESULTS = "run_results_v1"
    SOURCES = "sources_v1"

    @classmethod
    def get_destination_table(cls, artifact_type: ArtifactsTypesV1):
        """Get the destination table

        Args:
            artifact_type:

        Returns:
            (str) the destination BigQuery table ID
        """
        if artifact_type == ArtifactsTypesV1.CATALOG:
            return DestinationTablesV1.CATALOG
        elif artifact_type == ArtifactsTypesV1.MANIFEST:
            return DestinationTablesV1.MANIFEST
        elif artifact_type == ArtifactsTypesV1.RUN_RESULTS:
            return DestinationTablesV1.RUN_RESULTS
        elif artifact_type == ArtifactsTypesV1.SOURCES:
            return DestinationTablesV1.SOURCES
        else:
            raise ValueError("No such a artifact type: {}".format(artifact_type))


@dataclass
class CatalogV1:
    """Model class for catalog v1."""
    @classmethod
    def builder(cls):
        """Get a builder for catalog v1.

        Returns:
            a pointer of the class for catalog v1.
        """
        path = os.path.join(get_module_root(), "resources", "v1", "catalog.json")
        with open(path, "r") as fp:
            schema = json.load(fp)
        builder = pjs.ObjectBuilder(schema)
        ns = builder.build_classes()
        # pylint: disable=E1120
        return ns.getattr(ArtifactsTypesV1.CATALOG.value)


@dataclass
class ManifestV1:
    """Model class for manifest v1."""
    @classmethod
    def builder(cls):
        """Get a builder for manifest v1.

        Returns:
            a pointer of the class for manifest v1.
        """
        path = os.path.join(get_module_root(), "resources", "v1", "manifest.json")
        with open(path, "r") as fp:
            schema = json.load(fp)
        builder = pjs.ObjectBuilder(schema)
        ns = builder.build_classes()
        # pylint: disable=E1120
        return ns.getattr(ArtifactsTypesV1.MANIFEST.value)


@dataclass
class RunResultsV1:
    """Model class for run-results v1."""
    @classmethod
    def builder(cls):
        """Get a builder for run-results v1.

        Returns:
            a pointer of the class for run-results v1.
        """
        path = os.path.join(get_module_root(), "resources", "v1", "run-results.json")
        with open(path, "r") as fp:
            schema = json.load(fp)
        builder = pjs.ObjectBuilder(schema)
        ns = builder.build_classes()
        return ns.RunResults


@dataclass
class SourcesV1:
    """Model class for sources v1."""
    @classmethod
    def builder(cls):
        """Get a builder for sources v1.

        Returns:
            a pointer of the class for sources v1.
        """
        path = os.path.join(get_module_root(), "resources", "v1", "sources.json")
        with open(path, "r") as fp:
            schema = json.load(fp)
        builder = pjs.ObjectBuilder(schema)
        ns = builder.build_classes()
        # pylint: disable=E1120
        return ns.getattr(ArtifactsTypesV1.SOURCES.value)
