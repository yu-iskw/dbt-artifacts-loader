{% set project = var('project') %}
{% set dataset = var('dataset') %}

{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="expanded_run_results_v1",
    persist_docs={"relation": true, "columns": true},
    labels={
      "modeled_by": "dbt",
      "app": "dbt-artifacts-loader",
     },
  )
}}

WITH expanded_results AS (
  SELECT
    args.*,
    metadata.*,
    result.adapter_response AS adapter_response,
    result.unique_id AS unique_id,
    result.status AS status,
    result.execution_time AS execution_time,
    result.message AS message,
    result.timing AS timing,
  FROM {{ source(var('dataset'), 'run_results_v1') }}
        , UNNEST(results) AS result
)
, expanded_timing AS (
  SELECT
    fr.* EXCEPT (timing),
    expanded_timing.name AS timing_name,
    expanded_timing.completed_at AS completed_at,
    expanded_timing.started_at AS started_at,
  FROM expanded_results AS fr
       , UNNEST(timing) AS expanded_timing
)

SELECT
  *
FROM expanded_timing
