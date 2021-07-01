SELECT
  status
  , completed_at
  , unique_id
FROM {{ ref('flatten_run_results_v1') }}
WHERE
  rpc_method = "test"
  AND status = "fail"
  AND DATETIME(completed_at) BETWEEN DATETIME("{{ start_datetime }}:00") AND DATETIME("{{ end_datetime }}:00")
ORDER BY completed_at
