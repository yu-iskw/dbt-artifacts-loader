{% set project = var('dbt_artifacts_loader')['project'] %}
{% set dataset = var('dbt_artifacts_loader')['dataset'] %}

{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="latest_failed_source_freshness_v1",
    persist_docs={"relation": true, "columns": true},
    labels={
      "modeled_by": "dbt",
      "app": "dbt-artifacts-loader",
     },
  )
}}

WITH ranked_freshness AS (
  SELECT
    ROW_NUMBER() OVER (PARTITION BY unique_id ORDER BY generated_at DESC) AS rank,
    *
  FROM {{ ref("expanded_sources_v1") }}
)
, latest_failed_freshness AS (
  SELECT * EXCEPT (rank)
  FROM ranked_freshness
  WHERE
    rank = 1
    AND status IN ("runtime error", "error")
)

SELECT *
FROM latest_failed_freshness
