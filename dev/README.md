# Support new schemas

1. Download new schemas from [https://schemas.getdbt.com/](https://schemas.getdbt.com/).
2. Generate pydantic models by adding commands for new schemas in [generate-artifacts-models.sh](../dev/generate-artifacts-models.sh)
3. Manually add the `loaded_at` field to the new models.
4. Add values for the new schemas in [generate_bigquery_schemas.py](../dbt_artifacts_loader/scripts/generate_bigquery_schemas.py)
5. Generate BigQuery schemas by executing [generate-bigquery-schemas.sh](../dev/generate-bigquery-schemas.sh)
6. Add values corresponding to the new schemas in `dbt_artifacts_loader`.
7. Add testing artifacts by executing jaffle-shop with the new dbt version.
