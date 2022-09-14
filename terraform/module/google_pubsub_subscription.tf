resource "google_pubsub_subscription" "dbt_artifacts_notification_to_bigquery" {
  # If var.docker_image is null, then the subscription is not created.
  count = var.docker_image == null ? 0 : 1

  project = var.project_id

  name  = "${var.pubsub_topic}-to-bigquery"
  topic = google_pubsub_topic.dbt_artifacts_notification.id

  enable_exactly_once_delivery = false

  push_config {
    push_endpoint = "${google_cloud_run_service.dbt_artifact_loader[0].status[0].url}/api/v2/"

    oidc_token {
      service_account_email = google_service_account.cloud_run_invoker.email
    }
  }

  dead_letter_policy {
    dead_letter_topic     = google_pubsub_topic.dbt_artifacts_notification_deadletter.id
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
