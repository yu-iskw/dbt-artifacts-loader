DOCKER_IMAGE_BASE = gcr.io/ubie-yu-sandbox/dbt-artifacts-loader
TAG = "v1.0.0-rc1"


.PHONEY: setup
setup:
	bash ./ci/setup.sh

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
	ENV_FILE=".env/.env.local" uvicorn dbt_artifacts_loader.api.rest_api_v2:app

build-docker:
	docker build --rm -f ./Dockerfile  -t "$(DOCKER_IMAGE_BASE):$(TAG)" .

run-docker:
	docker run --rm -p 8080:80 "$(DOCKER_IMAGE_BASE):$(TAG)"

push-docker:
	docker push "$(DOCKER_IMAGE_BASE):$(TAG)"
