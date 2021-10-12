//resource "google_pubsub_subscription_iam_member" "editor" {
//  subscription = google_pubsub_subscription.dbt_artifacts_notification_deadletter_pool.id
//  role         = "roles/pubsub.subscriber"
//  member       = "serviceAccount:service-${data.google_project.project.number}@gcp-sa-pubsub.iam.gserviceaccount.com"
//}
