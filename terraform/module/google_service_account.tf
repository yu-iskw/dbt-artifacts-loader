resource "google_service_account" "dbt_artifacts_loader_cloud_run" {
  project = var.project_id

  account_id   = "${var.cloud_run_service_name}-cloud-run"
  display_name = "${var.cloud_run_service_name}-cloud-run"
  description  = "The service account is used for the REST API on Cloud Run"
}

resource "google_service_account" "cloud_run_invoker" {
  project = var.project_id

  account_id   = "${var.cloud_run_service_name}-invoker"
  display_name = "${var.cloud_run_service_name}-invoker"
  description  = "The service account is used to invoke the Cloud Run application from Cloud Pub/Sub"
}
