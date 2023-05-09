PROJECT_ID = YOUR-GCP-PROJECT
TAG = v1.8.0-dev2
DOCKER_IMAGE_BASE = gcr.io/$(PROJECT_ID)/dbt-artifacts-loader


.PHONEY: setup
setup: setup-python setup-pre-commit

.PHONE: setup-python
setup-python:
	bash ./ci/setup.sh

.PHONY: setup-pre-commit
setup-pre-commit:
	pre-commit install

lint: lint-python

lint-python:
	bash ci/lint_python.sh

format: format-terraform

format-terraform:
	terraform fmt --recursive terraform

test: test-python

test-python:
	bash ci/run_python_tests.sh

.PHONY: launch-locally
launch-locally:
	ENV_FILE=".env/.env.local" uvicorn dbt_artifacts_loader.api.rest_api_v2:app  --port 8080

build-docker:
	docker build --rm --platform linux/amd64 -f ./Dockerfile  -t "$(DOCKER_IMAGE_BASE):$(TAG)" .

run-docker:
	docker run --rm -p 8080:80 "$(DOCKER_IMAGE_BASE):$(TAG)"

push-docker:
	docker push "$(DOCKER_IMAGE_BASE):$(TAG)"

generate-models:
	bash dev/generate-artifacts-models.sh

generate-bq-schemas:
	bash dev/generate-bigquery-schemas.sh
