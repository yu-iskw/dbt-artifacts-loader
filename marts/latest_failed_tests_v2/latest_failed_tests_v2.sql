{% set project = var('dbt_artifacts_loader')['project'] %}
{% set dataset = var('dbt_artifacts_loader')['dataset'] %}

{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="latest_failed_tests_v2",
    persist_docs={"relation": true, "columns": true},
    labels={
      "modeled_by": "dbt",
      "app": "dbt-artifacts-loader",
     },
  )
}}

WITH ranked_tests AS (
  SELECT
    ROW_NUMBER() OVER (PARTITION BY unique_id ORDER BY completed_at DESC) AS rank,
    *
  FROM {{ ref("expanded_run_results_v2") }}
  WHERE
    timing_name = "execute"
    AND rpc_method IN ("test")
)
, latest_failed_tests AS (
  SELECT * EXCEPT (rank)
  FROM ranked_tests
  WHERE
      rank = 1 AND LOWER(status) = "fail"
)

SELECT *
FROM latest_failed_tests
