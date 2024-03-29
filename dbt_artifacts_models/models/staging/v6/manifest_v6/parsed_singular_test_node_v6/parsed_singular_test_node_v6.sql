{% set project = var('dbt_artifacts_loader')['project'] %}
{% set dataset = var('dbt_artifacts_loader')['dataset'] %}

{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="parsed_singular_test_node_v6",
    persist_docs={"relation": true, "columns": true},
    labels={
      "modeled_by": "dbt",
      "app": "dbt-artifacts-loader",
     },
  )
}}

WITH singular_tests AS (
  SELECT
    s.* EXCEPT(depends_on),
    depends_on_node,
    depends_on_macro,
  FROM (
      SELECT
        loaded_at AS loaded_at,
        metadata AS metadata,
        node.key AS key,
        node.value.ParsedSingularTestNode.*,
      FROM {{ source(var('dbt_artifacts_loader')['dataset'], 'manifest_v6') }}
            , UNNEST(nodes) AS node
  ) AS s
  CROSS JOIN UNNEST(depends_on.nodes.value) AS depends_on_node
  CROSS JOIN UNNEST(depends_on.macros.value) AS depends_on_macro
)
, singular_tests_with_models AS (
  SELECT
    singular_tests.*,
    (SELECT AS STRUCT models.*) AS depends_on_model,
  FROM singular_tests AS singular_tests
  LEFT OUTER JOIN {{ ref("parsed_model_node_v6") }} AS models
    ON singular_tests.metadata.invocation_id = models.metadata.invocation_id
        AND singular_tests.depends_on_node = models.unique_id
)
, remove_duplicates AS (
  SELECT
    ROW_NUMBER() OVER (PARTITION BY metadata.invocation_id, unique_id ORDER BY metadata.generated_at DESC) AS rank,
    *
  FROM singular_tests_with_models
  WHERE unique_id IS NOT NULL
)

SELECT
  * EXCEPT(rank)
FROM remove_duplicates
WHERE rank = 1
