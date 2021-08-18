{% set project = var('project') %}
{% set dataset = var('dataset') %}

{{
  config(
    enabled=true,
    full_refresh=none,
    materialized="view",
    database=project,
    schema=dataset,
    alias="latest_failed_results_v1",
    persist_docs={"relation": true, "columns": true},
    labels={
      "modeled_by": "dbt",
      "app": "dbt-artifacts-loader",
     },
  )
}}

SELECT *
FROM {{ ref("expanded_run_results_v1") }}
WHERE
timing_name = "execute"
AND rpc_method IN ("test")
AND LOWER(status) = "fail"
