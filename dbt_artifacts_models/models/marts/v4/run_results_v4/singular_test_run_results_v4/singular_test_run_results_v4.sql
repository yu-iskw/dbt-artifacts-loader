{% set dbt_minor_version = get_dbt_minor_version(version=dbt_version) %}

{% set project = var('dbt_artifacts_loader')['project'] %}
{% set dataset = var('dbt_artifacts_loader')['dataset'] %}


{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="singular_test_run_results_v4",
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
    (SELECT AS STRUCT singular_tests.*) AS singular_test,
  FROM {{ ref("expanded_run_results_v4") }} AS run_results
  {% if dbt_minor_version == "1.0" %}
  LEFT OUTER JOIN {{ ref("parsed_singular_test_node_v4") }} AS singular_tests
    ON run_results.unique_id = singular_tests.unique_id
      AND ABS(DATETIME_DIFF(run_results.metadata.generated_at, singular_tests.metadata.generated_at, DAY))  <= 2
  {% elif dbt_minor_version == "1.1" %}
  LEFT OUTER JOIN {{ ref("parsed_singular_test_node_v5") }} AS singular_tests
    ON run_results.unique_id = singular_tests.unique_id
      AND ABS(DATETIME_DIFF(run_results.metadata.generated_at, singular_tests.metadata.generated_at, DAY))  <= 2
  {% elif dbt_minor_version == "1.2" %}
  LEFT OUTER JOIN {{ ref("parsed_singular_test_node_v6") }} AS singular_tests
    ON run_results.unique_id = singular_tests.unique_id
      AND ABS(DATETIME_DIFF(run_results.metadata.generated_at, singular_tests.metadata.generated_at, DAY))  <= 2
  {% else %}
    {{ exceptions.raise_compiler_error("Unexpected dbt version: " ~ dbt_minor_version) }}
  {% endif %}
  WHERE singular_tests.unique_id IS NOT NULL
    AND timing_name IN ("execute")
)
-- Extract only run results whose metadata is the most close to that of model.
, nearest_manifests AS (
  SELECT
    ROW_NUMBER() OVER (PARTITION BY unique_id, metadata.invocation_id ORDER BY generated_at_diff) AS rank,
    * EXCEPT(generated_at_diff)
  FROM (
      SELECT
        ABS(DATETIME_DIFF(metadata.generated_at, singular_test.metadata.generated_at, SECOND)) AS generated_at_diff,
        *,
      FROM run_results
  )
)

SELECT
  * EXCEPT(rank)
FROM nearest_manifests
WHERE rank = 1
