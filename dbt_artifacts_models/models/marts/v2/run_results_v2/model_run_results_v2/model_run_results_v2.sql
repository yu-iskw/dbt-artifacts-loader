{% set project = var('dbt_artifacts_loader')['project'] %}
{% set dataset = var('dbt_artifacts_loader')['dataset'] %}

{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="model_run_results_v2",
    persist_docs={"relation": true, "columns": true},
    labels={
      "modeled_by": "dbt",
      "app": "dbt-artifacts-loader",
     },
  )
}}

WITH run_results AS (
  SELECT
    run_results.*,
    (SELECT AS STRUCT models.*) AS model,
  FROM {{ ref("expanded_run_results_v2") }} AS run_results
  FULL OUTER JOIN {{ ref("parsed_model_node_v2") }} AS models
    ON run_results.unique_id = models.unique_id
      AND ABS(DATETIME_DIFF(run_results.metadata.generated_at, models.metadata.generated_at, DAY))  <= 2
  WHERE models.unique_id IS NOT NULL
    AND timing_name IN ("execute")
)
-- Extract only run results whose metadata is the most close to that of model.
, nearest_manifests AS (
  SELECT
    ROW_NUMBER() OVER (PARTITION BY unique_id, metadata.invocation_id ORDER BY generated_at_diff) AS rank,
    * EXCEPT(generated_at_diff)
  FROM (
      SELECT
        ABS(DATETIME_DIFF(metadata.generated_at, model.metadata.generated_at, SECOND)) AS generated_at_diff,
        *,
      FROM run_results
  )
)

SELECT
  * EXCEPT(rank)
FROM nearest_manifests
WHERE rank = 1
