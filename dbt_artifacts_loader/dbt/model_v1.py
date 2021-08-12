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

import python_jsonschema_objects as pjs

from dbt_artifacts_loader.dbt.utils import ArtifactsTypes
from dbt_artifacts_loader.utils import get_module_root


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
        return ns.getattr(ArtifactsTypes.CATALOG_V1.value)


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
        return ns.getattr(ArtifactsTypes.MANIFEST_V1.value)


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
        return ns.getattr(ArtifactsTypes.SOURCES_V1.value)
