locals {
  bucket_location = (var.bucket_location != null ? var.bucket_location : var.region)
  bucket_name     = (var.bucket != null ? var.bucket : "${var.project_id}-dbt-artifacts")
}

resource "google_storage_bucket" "dbt_artifacts" {
  project  = var.project_id
  name     = local.bucket_name
  location = local.bucket_location

  force_destroy = var.delete_on_destroy

  uniform_bucket_level_access = true

  versioning {
    enabled = false
  }

  lifecycle_rule {
    condition {
      age = var.lifecycle_rule.condition.age
    }
    action {
      type          = var.lifecycle_rule.action.type
      storage_class = var.lifecycle_rule.action.storage_class
    }
  }

  labels = var.labels
}
