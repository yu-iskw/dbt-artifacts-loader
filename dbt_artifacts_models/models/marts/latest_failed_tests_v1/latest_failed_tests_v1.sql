{% set project = var('project') %}
{% set dataset = var('dataset') %}

{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="latest_failed_tests_v1",
    persist_docs={"relation": true, "columns": true},
    labels={
      "modeled_by": "dbt",
      "app": "dbt-artifacts-loader",
     },
  )
}}

WITH latest_failed_tests AS (
  SELECT
    ROW_NUMBER() OVER (PARTITION BY unique_id ORDER BY completed_at DESC) AS rank,
    *
  FROM {{ ref("expanded_run_results_v1") }}
  WHERE
    timing_name = "execute"
    AND rpc_method IN ("test")
    AND LOWER(status) = "fail"
)

SELECT
  * EXCEPT (rank)
FROM latest_failed_tests
WHERE rank = 1