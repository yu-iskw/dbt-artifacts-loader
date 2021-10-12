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

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# v1
generate-schema --keep_nulls < "${PROJECT_DIR}/tests/resources/v1/jaffle_shop/run_results.json" > "${PROJECT_DIR}/terraform/module/table_schemas/v1/run_results.json" || :
generate-schema --keep_nulls < "${PROJECT_DIR}/tests/resources/v1/jaffle_shop/manifest.json" > "${PROJECT_DIR}/terraform/module/table_schemas/v1/manifest.json" || :
generate-schema --keep_nulls < "${PROJECT_DIR}/tests/resources/v1/jaffle_shop/catalog.json" > "${PROJECT_DIR}/terraform/module/table_schemas/v1/catalog.json" || :
generate-schema --keep_nulls < "${PROJECT_DIR}/tests/resources/v1/jaffle_shop/sources.json" > "${PROJECT_DIR}/terraform/module/table_schemas/v1/sources.json" || :

# v2
generate-schema --keep_nulls < "${PROJECT_DIR}/tests/resources/v2/jaffle_shop/manifest.json" > "${PROJECT_DIR}/terraform/module/table_schemas/v2/manifest.json" || :
generate-schema --keep_nulls < "${PROJECT_DIR}/tests/resources/v2/jaffle_shop/run_results.json" > "${PROJECT_DIR}/terraform/module/table_schemas/v2/run_results.json" || :
