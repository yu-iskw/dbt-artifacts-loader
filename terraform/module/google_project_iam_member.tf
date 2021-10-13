resource "google_project_iam_member" "cloud_run" {
  for_each = toset([
    "roles/bigquery.jobUser",
  ])
  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.dbt_artifacts_loader_cloud_run.email}"
}

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
