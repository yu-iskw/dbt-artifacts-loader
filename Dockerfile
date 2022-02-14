FROM python:3.9.5

WORKDIR /app
EXPOSE 8080

# Set up
COPY requirements/* /app/requirements/
COPY ci/setup.sh /app/ci/setup.sh
RUN bash ci/setup.sh

COPY . /app

CMD ["uvicorn", "dbt_artifacts_loader.api.rest_api_v2:app", "--host", "0.0.0.0", "--port", "8080"]
