resource "google_pubsub_topic" "dbt_artifacts_notification" {
  project = var.project_id

  name   = var.pubsub_topic
  labels = var.labels
}

resource "google_pubsub_topic" "dbt_artifacts_notification_deadletter" {
  project = var.project_id

  name   = "${var.pubsub_topic}-deadletter"
  labels = var.labels
}
