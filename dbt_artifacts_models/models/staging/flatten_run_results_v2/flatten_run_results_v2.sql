{% set project = var('project') %}
{% set dataset = var('dataset') %}

{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="flatten_run_results_v2",
    persist_docs={"relation": true, "columns": true},
    labels={
      "modeled_by": "dbt",
      "app": "dbt-artifacts-loader",
     },
  )
}}

WITH flatten_results AS (
  SELECT
    args.*,
    metadata.*,
    result.adapter_response AS adapter_response,
    result.unique_id AS unique_id,
    result.status AS status,
    result.execution_time AS execution_time,
    result.message AS message,
    result.timing AS timing,
  FROM {{ source(var('dataset'), 'run_results_v2') }}
        , UNNEST(results) AS result
)
, flatten_timing AS (
  SELECT
    fr.* EXCEPT (timing),
    flatten_timing.name AS timing_name,
    flatten_timing.completed_at AS completed_at,
    flatten_timing.started_at AS started_at,
  FROM flatten_results AS fr
       , UNNEST(timing) AS flatten_timing
)

SELECT
  *
FROM flatten_timing
