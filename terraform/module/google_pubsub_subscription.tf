resource "google_pubsub_subscription" "dbt_artifacts_notification_to_bigquery" {
  project = var.project_id

  name  = "${var.pubsub_topic}-to-bigquery"
  topic = google_pubsub_topic.dbt_artifacts_notification.id

  push_config {
    push_endpoint = "${google_cloud_run_service.dbt_artifact_loader.status[0].url}/api/v1/"

    oidc_token {
      service_account_email = google_service_account.cloud_run_invoker.email
    }
  }

  labels = var.labels
}
