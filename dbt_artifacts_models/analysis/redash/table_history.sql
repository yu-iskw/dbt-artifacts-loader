WITH stats AS (
  SELECT
    invocation_id
    , generated_at
    , status
    , SUM(IF(status = "fail", 1, 0)) AS total_failed_tests
  FROM {{ ref('expanded_run_results_v1') }}
  WHERE
    rpc_method = "test"
    AND unique_id LIKE "%{{ model_id_pattern }}%"
    AND DATETIME(completed_at) BETWEEN DATETIME("{{ start_datetime }}:00") AND DATETIME("{{ end_datetime }}:00")
  GROUP BY 1, 2, 3
)

SELECT
  generated_at
  , total_failed_tests
FROM stats
ORDER BY generated_at
