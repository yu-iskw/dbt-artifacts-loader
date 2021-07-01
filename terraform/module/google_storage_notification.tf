resource "google_storage_notification" "notification" {
  bucket         = google_storage_bucket.dbt_artifacts.name
  payload_format = "JSON_API_V1"
  topic          = google_pubsub_topic.dbt_artifacts_notification.id
  event_types    = ["OBJECT_FINALIZE"]

  # custom_attributes = {
  #   new-attribute = "new-attribute-value"
  # }
  depends_on = [google_pubsub_topic_iam_binding.binding]
}
