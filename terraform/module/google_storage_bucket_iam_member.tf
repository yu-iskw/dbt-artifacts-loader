resource "google_storage_bucket_iam_member" "cloud_run_is_bucket_object_viewer" {
  bucket = google_storage_bucket.dbt_artifacts.name
  role   = "roles/storage.admin"
  member = "serviceAccount:${google_service_account.dbt_artifacts_loader_cloud_run.email}"
}

resource "google_storage_bucket_iam_member" "bucket_writers" {
  for_each = toset(var.bucket_writers)

  bucket = google_storage_bucket.dbt_artifacts.name
  role   = "roles/storage.admin"
  member = each.key
}

resource "google_storage_bucket_iam_member" "bucket_readers" {
  for_each = toset(var.bucket_readers)

  bucket = google_storage_bucket.dbt_artifacts.name
  role   = "roles/storage.objectViewer"
  member = each.key
}
