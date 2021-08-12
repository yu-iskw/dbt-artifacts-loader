#
# V1
#
resource "google_bigquery_table" "run_results_v1" {
  project = var.project_id

  dataset_id = google_bigquery_dataset.dbt_artifacts.dataset_id
  # NOTE The table ID must be the same as the python implementation.
  table_id      = "run_results_v1"
  friendly_name = "run_results_v1"
  description   = <<EOT
The table contains `run_results.json`.
EOT

  schema = file("${path.module}/table_schemas/v1/run_results.json")

  deletion_protection = (!var.delete_on_destroy)

  labels = var.labels
}

resource "google_bigquery_table" "sources_v1" {
  project = var.project_id

  dataset_id = google_bigquery_dataset.dbt_artifacts.dataset_id
  # NOTE The table ID must be the same as the python implementation.
  table_id      = "sources_v1"
  friendly_name = "sources_v1"
  description   = <<EOT
The table contains `sources.json`.
EOT

  schema = file("${path.module}/table_schemas/v1/sources.json")

  deletion_protection = (!var.delete_on_destroy)

  labels = var.labels
}

// The schema is not valid yet.
//resource "google_bigquery_table" "manifest_v1" {
//  project = var.project_id
//
//  dataset_id    = google_bigquery_dataset.dbt_artifacts.dataset_id
//  table_id      = "dbt_manifest_v1"
//  friendly_name = "dbt_manifest_v1"
//  description   = <<EOT
//The table contains `manifest.json`.
//EOT
//
//  schema = file("${path.module}/table_schemas/v1/manifest.json")
//
//  deletion_protection = var.delete_on_destroy
//
//  labels = var.labels
//}

#
# V2
#
resource "google_bigquery_table" "run_results_v2" {
  project = var.project_id

  dataset_id    = google_bigquery_dataset.dbt_artifacts.dataset_id
  # NOTE The table ID must be the same as the python implementation.
  table_id      = "run_results_v2"
  friendly_name = "run_results_v2"
  description   = <<EOT
The table contains `run_results.json`.
EOT

  schema = file("${path.module}/table_schemas/v2/run_results.json")

  deletion_protection = (! var.delete_on_destroy)

  labels = var.labels
}
