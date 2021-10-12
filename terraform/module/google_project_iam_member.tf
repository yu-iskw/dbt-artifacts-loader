resource "google_project_iam_member" "pubsub_service_account" {
  for_each = toset([
    "roles/iam.serviceAccountTokenCreator",
    "roles/pubsub.publisher",
    "roles/pubsub.subscriber",
  ])

  project = var.project_id
  role    = each.key
  member  = "serviceAccount:service-${data.google_project.project.number}@gcp-sa-pubsub.iam.gserviceaccount.com"
}
