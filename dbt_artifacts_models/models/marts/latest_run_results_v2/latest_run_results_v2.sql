{% set project = var('project') %}
{% set dataset = var('dataset') %}

{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="latest_run_results_v2",
    persist_docs={"relation": true, "columns": true},
    labels={
      "modeled_by": "dbt",
      "app": "dbt-artifacts-loader",
     },
  )
}}

WITH latest_run_results_v1 AS (
  SELECT
    ROW_NUMBER() OVER (PARTITION BY unique_id ORDER BY completed_at DESC) AS rank
    , invocation_id
    , dbt_version
    , rpc_method
    , unique_id
    , status
    , timing_name
    , completed_at
    , started_at
  FROM {{ ref("expanded_run_results_v2") }}
)

SELECT *
FROM latest_run_results_v1
WHERE rank = 1
