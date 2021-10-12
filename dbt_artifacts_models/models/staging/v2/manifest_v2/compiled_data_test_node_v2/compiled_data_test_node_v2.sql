{% set project = var('dbt_artifacts_loader')['project'] %}
{% set dataset = var('dbt_artifacts_loader')['dataset'] %}

{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="compiled_data_test_node_v2",
    persist_docs={"relation": true, "columns": true},
    labels={
      "modeled_by": "dbt",
      "app": "dbt-artifacts-loader",
     },
  )
}}

WITH data_tests AS (
  SELECT
    t.* EXCEPT(depends_on),
    depends_on_node,
    depends_on_macro,
  FROM (
      SELECT
        metadata AS metadata,
        node.key AS key,
        node.value.CompiledDataTestNode.*,
      FROM {{ source(var('dbt_artifacts_loader')['dataset'], 'manifest_v2') }}
            , UNNEST(nodes) AS node
  ) AS t
  CROSS JOIN UNNEST(depends_on.nodes.value) AS depends_on_node
  CROSS JOIN UNNEST(depends_on.macros.value) AS depends_on_macro
)
, data_tests_with_models AS (
  SELECT
    data_tests.*,
    (SELECT AS STRUCT models.*) AS depends_on_model,
  FROM data_tests AS data_tests
  LEFT OUTER JOIN {{ ref("compiled_model_node_v2") }} AS models
    ON data_tests.metadata.invocation_id = models.metadata.invocation_id
        AND data_tests.depends_on_node = models.unique_id
)
, remove_duplicates AS (
  SELECT
    ROW_NUMBER() OVER (PARTITION BY metadata.invocation_id, unique_id ORDER BY metadata.generated_at DESC) AS rank,
    *
  FROM data_tests_with_models
  WHERE unique_id IS NOT NULL
)

SELECT
  * EXCEPT(rank)
FROM remove_duplicates
WHERE rank = 1
