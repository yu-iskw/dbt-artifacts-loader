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

import os
import json
import click

from dbt_artifacts_loader.dbt.v1.catalog import CatalogV1
from dbt_artifacts_loader.dbt.v1.manifest import ManifestV1
from dbt_artifacts_loader.dbt.v1.run_results import RunResultsV1
from dbt_artifacts_loader.dbt.v1.sources import SourcesV1

from dbt_artifacts_loader.dbt.v2.manifest import ManifestV2
from dbt_artifacts_loader.dbt.v2.run_results import RunResultsV2
from dbt_artifacts_loader.dbt.v2.sources import SourcesV2

from dbt_artifacts_loader.dbt.v3.manifest import ManifestV3
from dbt_artifacts_loader.dbt.v3.run_results import RunResultsV3
from dbt_artifacts_loader.dbt.v3.sources import SourcesV3

from dbt_artifacts_loader.dbt.v4.manifest import ManifestV4
from dbt_artifacts_loader.dbt.v4.run_results import RunResultsV4

from dbt_artifacts_loader.dbt.v5.manifest import ManifestV5

from dbt_artifacts_loader.dbt.v6.manifest import ManifestV6
from dbt_artifacts_loader.dbt.v7.manifest import ManifestV7

from dbt_artifacts_loader.utils import get_project_root


resources_base_path = os.path.join(get_project_root(), "dbt_artifacts_loader", "resources")
table_schemas_base_path = os.path.join(get_project_root(), "terraform", "module", "table_schemas")

resources = [
    # v1
    {
        "class": CatalogV1,
        "output": os.path.join(table_schemas_base_path, "v1", "catalog.json"),
    },
    {
        "class": ManifestV1,
        "output": os.path.join(table_schemas_base_path, "v1", "manifest.json"),
    },
    {
        "class": RunResultsV1,
        "output": os.path.join(table_schemas_base_path, "v1", "run_results.json"),
    },
    {
        "class": SourcesV1,
        "output": os.path.join(table_schemas_base_path, "v1", "sources.json"),
    },
    # v2
    {
        "class": ManifestV2,
        "output": os.path.join(table_schemas_base_path, "v2", "manifest.json"),
    },
    {
        "class": RunResultsV2,
        "output": os.path.join(table_schemas_base_path, "v2", "run_results.json"),
    },
    {
        "class": SourcesV2,
        "output": os.path.join(table_schemas_base_path, "v2", "sources.json"),
    },
    # v3
    {
        "class": ManifestV3,
        "output": os.path.join(table_schemas_base_path, "v3", "manifest.json"),
    },
    {
        "class": RunResultsV3,
        "output": os.path.join(table_schemas_base_path, "v3", "run_results.json"),
    },
    {
        "class": SourcesV3,
        "output": os.path.join(table_schemas_base_path, "v3", "sources.json"),
    },
    # v4
    {
        "class": ManifestV4,
        "output": os.path.join(table_schemas_base_path, "v4", "manifest.json"),
    },
    {
        "class": RunResultsV4,
        "output": os.path.join(table_schemas_base_path, "v4", "run_results.json"),
    },
    # v5
    {
        "class": ManifestV5,
        "output": os.path.join(table_schemas_base_path, "v5", "manifest.json"),
    },
    # v6
    {
        "class": ManifestV6,
        "output": os.path.join(table_schemas_base_path, "v6", "manifest.json"),
    },
    # v7
    {
        "class": ManifestV7,
        "output": os.path.join(table_schemas_base_path, "v7", "manifest.json"),
    },
    # v8
    {
        "class": ManifestV8,
        "output": os.path.join(table_schemas_base_path, "v8", "manifest.json"),
    },
]


@click.command()
def main():
    for resource in resources:
        klass = resource["class"]
        output = resource["output"]
        # Load the JSON schema
        schema_fields = klass.to_bigquery_schema(depth=1)
        bigquery_schema = [x.to_api_repr() for x in schema_fields]
        with open(output, "w", encoding="utf-8") as fp:
            json.dump(bigquery_schema, fp, indent=2)


if __name__ == "__main__":
    main()
