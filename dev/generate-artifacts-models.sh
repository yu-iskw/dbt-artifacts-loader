#!/bin/bash

#
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
#
set -e

base_class="dbt_artifacts_loader.dbt.base_bigquery_model.BaseBigQueryModel"

# v1
datamodel-codegen  --input-file-type jsonschema \
  --base-class "$base_class" \
  --class-name "CatalogV1" \
  --input "dbt_artifacts_loader/resources/v1/catalog.json" \
  --output "dbt_artifacts_loader/dbt/v1/catalog.py"
datamodel-codegen  --input-file-type jsonschema \
  --base-class "$base_class" \
  --class-name "ManifestV1" \
  --input "dbt_artifacts_loader/resources/v1/manifest.json" \
  --output "dbt_artifacts_loader/dbt/v1/manifest.py"
datamodel-codegen  --input-file-type jsonschema \
  --base-class "$base_class" \
  --class-name "RunResultsV1" \
  --input "dbt_artifacts_loader/resources/v1/run-results.json" \
  --output "dbt_artifacts_loader/dbt/v1/run_results.py"
datamodel-codegen  --input-file-type jsonschema \
  --base-class "$base_class" \
  --class-name "SourcesV1" \
  --input "dbt_artifacts_loader/resources/v1/sources.json" \
  --output "dbt_artifacts_loader/dbt/v1/sources.py"

# v2
datamodel-codegen  --input-file-type jsonschema \
  --base-class "$base_class" \
  --class-name "ManifestV2" \
  --input "dbt_artifacts_loader/resources/v2/manifest.json" \
  --output "dbt_artifacts_loader/dbt/v2/manifest.py"
datamodel-codegen  --input-file-type jsonschema \
  --base-class "$base_class" \
  --class-name "RunResultsV2" \
  --input "dbt_artifacts_loader/resources/v2/run-results.json" \
  --output "dbt_artifacts_loader/dbt/v2/run_results.py"
datamodel-codegen  --input-file-type jsonschema \
  --base-class "$base_class" \
  --class-name "SourcesV2" \
  --input "dbt_artifacts_loader/resources/v2/sources.json" \
  --output "dbt_artifacts_loader/dbt/v2/sources.py"

# v3
datamodel-codegen  --input-file-type jsonschema \
  --base-class "$base_class" \
  --class-name "ManifestV3" \
  --input "dbt_artifacts_loader/resources/v3/manifest.json" \
  --output "dbt_artifacts_loader/dbt/v3/manifest.py"
datamodel-codegen  --input-file-type jsonschema \
  --base-class "$base_class" \
  --class-name "RunResultsV3" \
  --input "dbt_artifacts_loader/resources/v3/run-results.json" \
  --output "dbt_artifacts_loader/dbt/v3/run_results.py"
datamodel-codegen  --input-file-type jsonschema \
  --base-class "$base_class" \
  --class-name "SourcesV3" \
  --input "dbt_artifacts_loader/resources/v3/sources.json" \
  --output "dbt_artifacts_loader/dbt/v3/sources.py"

# v4
datamodel-codegen  --input-file-type jsonschema \
  --base-class "$base_class" \
  --class-name "ManifestV4" \
  --input "dbt_artifacts_loader/resources/v4/manifest.json" \
  --output "dbt_artifacts_loader/dbt/v4/manifest.py"
datamodel-codegen  --input-file-type jsonschema \
  --base-class "$base_class" \
  --class-name "RunResultsV4" \
  --input "dbt_artifacts_loader/resources/v4/run-results.json" \
  --output "dbt_artifacts_loader/dbt/v4/run_results.py"

# v5
datamodel-codegen  --input-file-type jsonschema \
  --base-class "$base_class" \
  --class-name "ManifestV5" \
  --input "dbt_artifacts_loader/resources/v5/manifest.json" \
  --output "dbt_artifacts_loader/dbt/v5/manifest.py"
