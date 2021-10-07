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

# v1
datamodel-codegen  --input-file-type jsonschema \
  --input "dbt_artifacts_loader/resources/v1/catalog.json" \
  --output "dbt_artifacts_loader/dbt/v1/catalog.py"
datamodel-codegen  --input-file-type jsonschema \
  --input "dbt_artifacts_loader/resources/v1/manifest.json" \
  --output "dbt_artifacts_loader/dbt/v1/manifest.py"
datamodel-codegen  --input-file-type jsonschema \
  --input "dbt_artifacts_loader/resources/v1/run-results.json" \
  --output "dbt_artifacts_loader/dbt/v1/run_results.py"
datamodel-codegen  --input-file-type jsonschema \
  --input "dbt_artifacts_loader/resources/v1/sources.json" \
  --output "dbt_artifacts_loader/dbt/v1/sources.py"

# v2
datamodel-codegen  --input-file-type jsonschema \
  --input "dbt_artifacts_loader/resources/v2/manifest.json" \
  --output "dbt_artifacts_loader/dbt/v2/manifest.py"
datamodel-codegen  --input-file-type jsonschema \
  --input "dbt_artifacts_loader/resources/v2/run-results.json" \
  --output "dbt_artifacts_loader/dbt/v2/run_results.py"