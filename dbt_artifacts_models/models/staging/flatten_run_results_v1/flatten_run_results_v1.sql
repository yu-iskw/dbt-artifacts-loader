{% set project = var('project') %}
{% set dataset = var('dataset') %}

{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="flatten_run_results_v1",
    persist_docs={"relation": true, "columns": true},
    labels={
      "modeled_by": "dbt",
      "app": "dbt-artifacts-loader",
     },
  )
}}

WITH flatten_results AS (
  SELECT
    metadata.invocation_id AS invocation_id
    , metadata.generated_at AS generated_at
    , metadata.dbt_version AS dbt_version
    , args.rpc_method AS rpc_method
    , result.unique_id AS unique_id
    , result.status AS status
    , result.execution_time AS execution_time
    , result.message AS message
    , result.timing AS timing
  FROM {{ source(var('dataset'), 'run_results_v1') }}
        , UNNEST(results) AS result
)
, flatten_timing AS (
  SELECT
    ROW_NUMBER() OVER (PARTITION BY invocation_id, unique_id ORDER BY flatten_timing.completed_at DESC) AS rank
    , invocation_id
    , generated_at
    , dbt_version
    , rpc_method
    , unique_id
    , status
    , flatten_timing.name AS timing_name
    , flatten_timing.completed_at AS completed_at
    , flatten_timing.started_at AS started_at
  FROM flatten_results, UNNEST(timing) AS flatten_timing
)

SELECT
  *
FROM flatten_timing
WHERE
  rank = 1
  AND timing_name = "execute"
