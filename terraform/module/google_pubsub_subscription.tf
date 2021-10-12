resource "google_pubsub_subscription" "dbt_artifacts_notification_to_bigquery" {
  project = var.project_id

  name  = "${var.pubsub_topic}-to-bigquery"
  topic = google_pubsub_topic.dbt_artifacts_notification.id

  push_config {
    push_endpoint = "${google_cloud_run_service.dbt_artifact_loader.status[0].url}/api/v2/"

    oidc_token {
      service_account_email = google_service_account.cloud_run_invoker.email
    }
  }

  dead_letter_policy {
    dead_letter_topic = google_pubsub_topic.dbt_artifacts_notification_deadletter.id
    max_delivery_attempts = 5
  }

  labels = var.labels
}

resource "google_pubsub_subscription" "dbt_artifacts_notification_deadletter_pool" {
  project = var.project_id

  name  = "${var.pubsub_topic}-deadletter-pool"
  topic = google_pubsub_topic.dbt_artifacts_notification_deadletter.id

  labels = var.labels
}
