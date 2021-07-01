resource "google_storage_bucket_iam_member" "cloud_run_is_bucket_object_viewer" {
  bucket = google_storage_bucket.dbt_artifacts.name
  role   = "roles/storage.admin"
  member = "serviceAccount:${google_service_account.dbt_artifacts_loader_cloud_run.email}"
}
