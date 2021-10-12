locals {
  v1_tables = {
    # table_id: JSON file
    catalog_v1: "catalog.json"
    run_results_v1: "run_results.json"
    manifest_v1: "manifest.json"
    sources_v1: "sources.json"
  }
  v2_tables = {
    # table_id: JSON file
    run_results_v2: "run_results.json"
    manifest_v2: "manifest.json"
  }
}

resource "google_bigquery_table" "v1_tables" {
  for_each = local.v1_tables

  project = var.project_id

  dataset_id = google_bigquery_dataset.dbt_artifacts.dataset_id
  # NOTE The table ID must be the same as the python implementation.
  table_id      = each.key
  friendly_name = each.key
  description   = <<EOT
The table derives from `${each.value}`.
EOT

  schema = file("${path.module}/table_schemas/v1/${each.value}")

  deletion_protection = (!var.delete_on_destroy)

  labels = var.labels
}

resource "google_bigquery_table" "v2_tables" {
  for_each = local.v2_tables

  project = var.project_id

  dataset_id = google_bigquery_dataset.dbt_artifacts.dataset_id
  # NOTE The table ID must be the same as the python implementation.
  table_id      = each.key
  friendly_name = each.key
  description   = <<EOT
The table derives from `${each.value}`.
EOT

  schema = file("${path.module}/table_schemas/v2/${each.value}")

  deletion_protection = (!var.delete_on_destroy)

  labels = var.labels
}
