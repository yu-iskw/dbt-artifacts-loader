setup:
	pip install -r requirements.txt
	dbt clean
	dbt deps

build:
	dbt build --profiles-dir ./profiles --selector dbt-1.5

run:
	dbt run --profiles-dir ./profiles --selector dbt-1.5

compile:
	dbt compile --profiles-dir ./profiles

test:
	dbt test --profiles-dir profiles/ --selector dbt-1.5

docs-generate:
	dbt docs generate --profiles-dir profiles/

docs-serve:
	dbt docs serve --profiles-dir profiles/
