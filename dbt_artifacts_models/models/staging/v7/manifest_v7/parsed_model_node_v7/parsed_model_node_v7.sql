{% set project = var('dbt_artifacts_loader')['project'] %}
{% set dataset = var('dbt_artifacts_loader')['dataset'] %}

{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="parsed_model_node_v7",
    persist_docs={"relation": true, "columns": true},
    labels={
      "modeled_by": "dbt",
      "app": "dbt-artifacts-loader",
     },
  )
}}

WITH expanded_artifacts AS (
  SELECT
    loaded_at AS loaded_at,
    metadata AS metadata,
    node.key AS key,
    node.value.ParsedModelNode.*,
  FROM {{ source(var('dbt_artifacts_loader')['dataset'], 'manifest_v7') }}
        , UNNEST(nodes) AS node
)
, remove_duplicates AS (
  SELECT
    ROW_NUMBER() OVER (PARTITION BY metadata.invocation_id, unique_id ORDER BY metadata.generated_at DESC) AS rank,
    *
  FROM expanded_artifacts
  WHERE unique_id IS NOT NULL
)

SELECT
  * EXCEPT(rank)
FROM remove_duplicates
WHERE rank = 1
