{% set project = var('dbt_artifacts_loader')['project'] %}
{% set dataset = var('dbt_artifacts_loader')['dataset'] %}

{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="schema_test_run_results_v2",
    persist_docs={"relation": true, "columns": true},
    labels={
      "modeled_by": "dbt",
      "app": "dbt-artifacts-loader",
     },
  )
}}

WITH run_results AS (
  SELECT
    run_results.* EXCEPT(metadata),
    run_results.metadata AS run_results_metadata,
    schema_tests.* EXCEPT(unique_id, metadata),
    schema_tests.metadata AS schema_test_metadata,
  FROM {{ ref("expanded_run_results_v2") }} AS run_results
  LEFT OUTER JOIN {{ ref("parsed_schema_test_node_v2") }} AS schema_tests
    ON run_results.unique_id = schema_tests.unique_id
  WHERE schema_tests.unique_id IS NOT NULL
    AND timing_name IN ("execute")
)
-- Extract only run results whose metadata is the most close to that of model.
, nearest_manifests AS (
  SELECT
    ROW_NUMBER() OVER (PARTITION BY unique_id ORDER BY generated_at_diff) AS rank,
    * EXCEPT(generated_at_diff)
  FROM (
      SELECT
        ABS(DATETIME_DIFF(run_results_metadata.generated_at, schema_test_metadata.generated_at, SECOND)) AS generated_at_diff,
        *,
      FROM run_results
  )
)

SELECT
  * EXCEPT(rank)
FROM nearest_manifests
WHERE rank = 1