#!/bin/bash
set -euo pipefail

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

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# dbt artifacts v1
v1_artifacts=("catalog" "manifest" "run-results" "sources")
for artifact in ${v1_artifacts[@]}
do
  echo "Converting ${artifact} v1"
  input="${PROJECT_DIR}/dbt_artifacts_loader/resources/v1/${artifact}.json"
  output="${PROJECT_DIR}/terraform/module/table_schemas/v1/${artifact}.json"
  tmp_file=".tmp.json"

  # Expand references in the JSON schema
  python "${PROJECT_DIR}/dev/expand_json_schema_references.py" --input "$input" --output "$tmp_file"

  # Convert the JSON schema to the BigQuery table schema
  jsbq --preventAdditionalObjectProperties \
      --continueOnError \
      -j "$tmp_file" > "$output"
done

# dbt artifacts v2
v2_artifacts=("manifest" "run-results")
for artifact in ${v2_artifacts[@]}
do
  echo "Converting ${artifact} v1"
  input="${PROJECT_DIR}/dbt_artifacts_loader/resources/v1/${artifact}.json"
  tmp_file=".tmp.json"
  output="${PROJECT_DIR}/terraform/module/table_schemas/v1/${artifact}.json"

  # Expand references in the JSON schema
  python "${PROJECT_DIR}/dev/expand_json_schema_references.py" --input "$input" --output "$tmp_file"

  # Convert the JSON schema to the BigQuery table schema
  jsbq --preventAdditionalObjectProperties \
      --continueOnError \
      -j "$tmp_file" > "$output"
done
