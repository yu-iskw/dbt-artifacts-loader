module "dbt_artifacts_loader" {
  source = "../module"

  project_id = var.project_id
  region     = var.region

  delete_on_destroy = true

  docker_image = "gcr.io/${var.project_id}/dbt-artifacts-loader:v1.0.0-rc1"

  labels = {
    app = "dbt-artifacts-loader"
  }
}

resource "google_service_account" "tmp_redash" {
  project = var.project_id

  account_id = "tmp-redash"
}

resource "google_project_iam_member" "tmp_redash_is_bq_admin" {
  for_each = toset([
    "roles/bigquery.dataViewer",
    "roles/bigquery.jobUser",
  ])

  project = var.project_id
  role    = each.key
  member  = "serviceAccount:${google_service_account.tmp_redash.email}"
}
