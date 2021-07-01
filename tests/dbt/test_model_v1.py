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

from dbt_artifacts_loader.dbt.model_v1 import RunResultsV1

from dbt_artifacts_loader.utils import get_project_root


class TestRunResultsV1(unittest.TestCase):

    def test_builder(self):
        klass = RunResultsV1.builder()
        test_json_path = os.path.join(get_project_root(), "tests", "resources", "v1", "jaffle_shop", "run_results.json")
        with open(test_json_path, "r") as fp:
            run_results_json = json.load(fp)
        run_results = klass(**run_results_json)
        self.assertDictEqual(run_results.as_dict(), run_results_json)


# class TestManifestV1(unittest.TestCase):
#
#     def test_builder(self):
#         klass = ManifestV1.builder()
#         test_json_path = os.path.join(get_project_root(), "tests", "resources", "v1", "jaffle_shop", "manifest.json")
#         with open(test_json_path, "r") as fp:
#             run_results_json = json.load(fp)
#         run_results = klass(**run_results_json)
#         self.assertDictEqual(run_results.as_dict(), run_results_json)
