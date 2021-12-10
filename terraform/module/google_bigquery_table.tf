locals {
  v1_tables = {
    # table_id: JSON file
    catalog_v1 : "catalog.json"
    run_results_v1 : "run_results.json"
    manifest_v1 : "manifest.json"
    sources_v1 : "sources.json"
  }
  v2_tables = {
    # table_id: JSON file
    run_results_v2 : "run_results.json"
    manifest_v2 : "manifest.json"
    sources_v2 : "sources.json"
  }
  v3_tables = {
    # table_id: JSON file
    run_results_v3 : "run_results.json"
    manifest_v3 : "manifest.json"
    sources_v3 : "sources.json"
  }
  v4_tables = {
    # table_id: JSON file
    run_results_v4 : "run_results.json"
    manifest_v4 : "manifest.json"
  }
}

resource "google_bigquery_table" "v1_tables" {
  for_each = local.v1_tables

  project = var.project_id

  deletion_protection = (!var.delete_on_destroy)

  dataset_id = google_bigquery_dataset.dbt_artifacts.dataset_id
  # NOTE The table ID must be the same as the python implementation.
  table_id      = each.key
  friendly_name = each.key
  description   = <<EOT
The table derives from `${each.value}`.
EOT

  schema = file("${path.module}/table_schemas/v1/${each.value}")

  time_partitioning {
    type  = "DAY"
    field = "loaded_at"
  }

  labels = var.labels
}

resource "google_bigquery_table" "v2_tables" {
  for_each = local.v2_tables

  project = var.project_id

  deletion_protection = (!var.delete_on_destroy)

  dataset_id = google_bigquery_dataset.dbt_artifacts.dataset_id
  # NOTE The table ID must be the same as the python implementation.
  table_id      = each.key
  friendly_name = each.key
  description   = <<EOT
The table derives from `${each.value}`.
EOT

  schema = file("${path.module}/table_schemas/v2/${each.value}")

  time_partitioning {
    type  = "DAY"
    field = "loaded_at"
  }

  labels = var.labels
}

resource "google_bigquery_table" "v3_tables" {
  for_each = local.v3_tables

  project = var.project_id

  deletion_protection = (!var.delete_on_destroy)

  dataset_id = google_bigquery_dataset.dbt_artifacts.dataset_id
  # NOTE The table ID must be the same as the python implementation.
  table_id      = each.key
  friendly_name = each.key
  description   = <<EOT
The table derives from `${each.value}`.
EOT

  schema = file("${path.module}/table_schemas/v3/${each.value}")

  time_partitioning {
    type  = "DAY"
    field = "loaded_at"
  }

  labels = var.labels
}

resource "google_bigquery_table" "v4_tables" {
  for_each = local.v4_tables

  project = var.project_id

  deletion_protection = (!var.delete_on_destroy)

  dataset_id = google_bigquery_dataset.dbt_artifacts.dataset_id
  # NOTE The table ID must be the same as the python implementation.
  table_id      = each.key
  friendly_name = each.key
  description   = <<EOT
The table derives from `${each.value}`.
EOT

  schema = file("${path.module}/table_schemas/v4/${each.value}")

  time_partitioning {
    type  = "DAY"
    field = "loaded_at"
  }

  labels = var.labels
}
