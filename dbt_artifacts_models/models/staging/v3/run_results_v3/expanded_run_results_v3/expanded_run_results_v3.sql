{% set project = var('dbt_artifacts_loader')['project'] %}
{% set dataset = var('dbt_artifacts_loader')['dataset'] %}

{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="expanded_run_results_v3",
    persist_docs={"relation": true, "columns": true},
    labels={
      "modeled_by": "dbt",
      "app": "dbt-artifacts-loader",
     },
  )
}}

WITH expanded_results AS (
  SELECT
    loaded_at AS loaded_at,
    STRUCT(
        JSON_EXTRACT_SCALAR(args, "$.selector_name") AS selector_name,
        JSON_EXTRACT_SCALAR(args, "$.profile") AS profile,
        JSON_EXTRACT_SCALAR(args, "$.target") AS target,
        JSON_EXTRACT_SCALAR(args, "$.rpc_method") AS rpc_method,
        JSON_EXTRACT_SCALAR(args, "$.vars") AS vars
    ) AS args,
    args AS raw_args,
    metadata,
    result.adapter_response AS adapter_response,
    result.unique_id AS unique_id,
    result.status AS status,
    result.execution_time AS execution_time,
    result.message AS message,
    result.timing AS timing,
  FROM {{ source(var('dbt_artifacts_loader')['dataset'], 'run_results_v3') }}
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
, remove_duplicates AS (
  SELECT
    ROW_NUMBER() OVER (PARTITION BY metadata.invocation_id, unique_id, timing_name ORDER BY metadata.generated_at DESC) AS rank,
    *
  FROM expanded_timing
)

SELECT
  * EXCEPT(rank)
FROM remove_duplicates
WHERE rank = 1
