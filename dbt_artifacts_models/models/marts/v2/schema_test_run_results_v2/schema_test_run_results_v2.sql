{% set project = var('dbt_artifacts_loader')['project'] %}
{% set dataset = var('dbt_artifacts_loader')['dataset'] %}

{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="schema_test_run_results_v2",
    persist_docs={"relation": true, "columns": true},
    labels={
      "modeled_by": "dbt",
      "app": "dbt-artifacts-loader",
     },
  )
}}

WITH schema_tests AS (
  SELECT
    * EXCEPT(depends_on, depends_on_macro, depends_on_node),
    depends_on_macro,
    depends_on_node,
  FROM {{ ref("parsed_schema_test_node_v2") }} AS schema_test_nodes
       CROSS JOIN UNNEST(depends_on.nodes.value) AS depends_on_node
       CROSS JOIN UNNEST(depends_on.macros.value) AS  depends_on_macro
)
, schema_tests_with_models AS (
  SELECT
    schema_tests.* EXCEPT(metadata),
    schema_tests.metadata AS schema_test_metadata,
    models.* EXCEPT(metadata, unique_id),
    models.metadata AS model_metadata,
    models.unique_id AS model_unique_id,
  FROM schema_tests AS schema_tests
  LEFT OUTER JOIN {{ ref("parsed_model_node_v2") }} AS models
    ON schema_tests.depends_on_node = models.unique_id
       AND schema_tests.metadata.invocation_id = models.metadata.invocation_id
)
, run_results AS (
  SELECT
    run_results.* EXCEPT(metadata),
    run_results.metadata AS run_results_metadata,
    schema_tests_with_models.* EXCEPT(unique_id),
  FROM {{ ref("expanded_run_results_v2") }} AS run_results
  LEFT OUTER JOIN schema_tests_with_models AS schema_tests_with_models
    ON run_results.unique_id = schema_tests_with_models.unique_id
  WHERE schema_tests_with_models.unique_id IS NOT NULL
)
, nearest_manifests AS (
  SELECT
    ROW_NUMBER() OVER (PARTITION BY unique_id ORDER BY generated_at_diff) AS rank,
    * EXCEPT(generated_at_diff)
  FROM (
      SELECT
        ABS(DATETIME_DIFF(run_results_metadata.generated_at, schema_test_metadata.generated_at, SECOND)) AS generated_at_diff,
        *,
      FROM run_results
  )
)

SELECT
  * EXCEPT(rank)
FROM nearest_manifests
WHERE rank = 1
