{% set project = var('dbt_artifacts_loader')['project'] %}
{% set dataset = var('dbt_artifacts_loader')['dataset'] %}

{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="source_freshness_runtime_error_v1",
    persist_docs={"relation": true, "columns": true},
    labels={
      "modeled_by": "dbt",
      "app": "dbt-artifacts-loader",
     },
  )
}}

WITH expanded_sources AS (
  SELECT
    elapsed_time,
    metadata.*,
    result.values.SourceFreshnessOutput.*,
  FROM {{ source(var('dbt_artifacts_loader')['dataset'], 'sources_v1') }}
        , UNNEST(results) AS result
)
, remove_duplicates AS (
  SELECT
    ROW_NUMBER() OVER (PARTITION BY invocation_id, unique_id ORDER BY generated_at DESC) AS rank,
    *,
  FROM expanded_sources
)

SELECT
  * EXCEPT(rank)
FROM remove_duplicates
WHERE rank = 1
