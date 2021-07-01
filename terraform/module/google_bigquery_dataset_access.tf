resource "google_bigquery_dataset_access" "cloud_run_is_dataset_owner" {
  project = var.project_id

  dataset_id    = google_bigquery_dataset.dbt_artifacts.dataset_id
  role          = "OWNER"
  user_by_email = google_service_account.dbt_artifacts_loader_cloud_run.email
}
