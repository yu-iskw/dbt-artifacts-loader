{% set project = var('dbt_artifacts_loader')['project'] %}
{% set dataset = var('dbt_artifacts_loader')['dataset'] %}

{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="data_test_run_results_v1",
    persist_docs={"relation": true, "columns": true},
    labels={
      "modeled_by": "dbt",
      "app": "dbt-artifacts-loader",
     },
  )
}}

WITH run_results AS (
  SELECT
    run_results.*,
    (SELECT AS STRUCT data_tests.*) AS data_test,
  FROM {{ ref("expanded_run_results_v1") }} AS run_results
  LEFT OUTER JOIN {{ ref("parsed_data_test_node_v1") }} AS data_tests
    ON run_results.unique_id = data_tests.unique_id
      AND ABS(DATETIME_DIFF(run_results.metadata.generated_at, data_tests.metadata.generated_at, DAY))  <= 2
  WHERE data_tests.unique_id IS NOT NULL
    AND timing_name IN ("execute")
)
-- Extract only run results whose metadata is the most close to that of model.
, nearest_manifests AS (
  SELECT
    ROW_NUMBER() OVER (PARTITION BY unique_id, metadata.invocation_id ORDER BY generated_at_diff) AS rank,
    * EXCEPT(generated_at_diff)
  FROM (
      SELECT
        ABS(DATETIME_DIFF(metadata.generated_at, data_test.metadata.generated_at, SECOND)) AS generated_at_diff,
        *,
      FROM run_results
  )
)

SELECT
  * EXCEPT(rank)
FROM nearest_manifests
WHERE rank = 1
