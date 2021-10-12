setup:
	dbt clean
	dbt deps

run:
	dbt run --profiles-dir ./profiles

compile:
	dbt compile --profiles-dir ./profiles

test:
	dbt test --profiles-dir profiles/

docs-generate:
	dbt docs generate --profiles-dir profiles/

docs-serve:
	dbt docs serve --profiles-dir profiles/
