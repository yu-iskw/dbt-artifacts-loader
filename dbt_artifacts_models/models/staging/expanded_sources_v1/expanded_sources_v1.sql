{% set project = var('project') %}
{% set dataset = var('dataset') %}

{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="expanded_sources_v1",
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
    result.*,
  FROM {{ source(var('dataset'), 'sources_v1') }}
        , UNNEST(results) AS result
)

SELECT
  *
FROM expanded_sources
