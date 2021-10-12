{% set project = var('dbt_artifacts_loader')['project'] %}
{% set dataset = var('dbt_artifacts_loader')['dataset'] %}

{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="model_run_results_v1",
    persist_docs={"relation": true, "columns": true},
    labels={
      "modeled_by": "dbt",
      "app": "dbt-artifacts-loader",
     },
  )
}}

WITH run_results AS (
  SELECT
    run_results.* EXCEPT(metadata),
    run_results.metadata AS run_results_metadata,
    manifest.* EXCEPT(metadata, unique_id   ),
    manifest.metadata AS manifest_metadata,
  FROM {{ ref("expanded_run_results_v1") }} AS run_results
  LEFT OUTER JOIN {{ ref("parsed_model_node_v1") }} AS manifest
    ON run_results.unique_id = manifest.unique_id
  WHERE manifest.unique_id IS NOT NULL
    AND timing_name IN ("execute")
)
, nearest_manifests AS (
  SELECT
    ROW_NUMBER() OVER (PARTITION BY unique_id ORDER BY generated_at_diff) AS rank,
    * EXCEPT(generated_at_diff)
  FROM (
      SELECT
        ABS(DATETIME_DIFF(run_results_metadata.generated_at, manifest_metadata.generated_at, SECOND)) AS generated_at_diff,
        *,
      FROM run_results
  )
)

SELECT
  * EXCEPT(rank)
FROM nearest_manifests
WHERE rank = 1
