#
# GCS
#
output "storage_name" {
  description = "The GCS bucket to store dbt artifacts"
  value       = google_storage_bucket.dbt_artifacts.name
}

#
# BigQuery
#
output "dataset_id" {
  description = "The BigQuery dataset ID to store dbt artifacts"
  value       = google_bigquery_dataset.dbt_artifacts.dataset_id
}
