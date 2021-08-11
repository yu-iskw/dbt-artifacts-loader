resource "google_pubsub_topic" "dbt_artifacts_notification" {
  project = var.project_id

  name   = var.pubsub_topic
  labels = var.labels
}
