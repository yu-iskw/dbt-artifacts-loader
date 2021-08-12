locals {
  bigquery_location = (var.bigquery_location == null ? var.region : var.bigquery_location)
}

resource "google_bigquery_dataset" "dbt_artifacts" {
  project = var.project_id

  dataset_id = var.bigquery_dataset_id
  location   = local.bigquery_location

  delete_contents_on_destroy = var.delete_on_destroy

  description = <<EOT
The dataset contains dbt artifacts.
EOT

  labels = var.labels
}
