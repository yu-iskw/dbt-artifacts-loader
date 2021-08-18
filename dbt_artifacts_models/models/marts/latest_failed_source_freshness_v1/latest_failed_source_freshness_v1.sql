{% set project = var('project') %}
{% set dataset = var('dataset') %}

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

WITH latest_failed_freshness AS (
  SELECT
    ROW_NUMBER() OVER (PARTITION BY unique_id ORDER BY generated_at DESC) AS rank,
    *
  FROM {{ ref("expanded_sources_v1") }}
  WHERE
    status NOT IN ("runtime error", "error")
)

SELECT
  * EXCEPT (rank)
FROM latest_failed_freshness
WHERE rank = 1
