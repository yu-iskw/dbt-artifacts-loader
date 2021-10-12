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
import json
import jsonref

import click


@click.command()
@click.option("--input", type=str, required=True, help="The path to the JSON schema file")
@click.option("--output", type=str, required=True, help="The path to the expanded output JSON schema file")
def cmd(input: str, output: str):
    """Expand references in the input JSON schema file

    Args:
        input (str): the path to the input JSON schema file
        output (str): the path to the output JSON schema file
    """
    with open(input, "r") as fp:
        data = jsonref.load(fp)
    with open(output, "w") as fp:
        json.dump(data, fp)


def main():
    cmd()


if __name__ == "__main__":
    main()
