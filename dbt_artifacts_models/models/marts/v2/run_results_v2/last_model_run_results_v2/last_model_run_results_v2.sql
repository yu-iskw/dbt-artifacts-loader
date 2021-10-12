{% set project = var('dbt_artifacts_loader')['project'] %}
{% set dataset = var('dbt_artifacts_loader')['dataset'] %}

{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="last_model_run_results_v2",
    persist_docs={"relation": true, "columns": true},
    labels={
      "modeled_by": "dbt",
      "app": "dbt-artifacts-loader",
     },
  )
}}

WITH run_results AS (
  SELECT
    ROW_NUMBER() OVER (PARTITION BY unique_id ORDER BY completed_at DESC) AS rank,
    *,
  FROM {{ ref("model_run_results_v2") }}
)

SELECT
  * EXCEPT(rank)
FROM run_results
WHERE rank = 1
