#
# Common
#
variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "default GCP region"
  type        = string
}

variable "delete_on_destroy" {
  description = "Delete GCS and BigQuery on terraform destroy"
  type        = bool
  default     = false
}

variable "labels" {
  description = "Labels for GCP resources"
  type        = map(string)
  default     = {}
}

#
# GCS
#
variable "bucket" {
  description = "GCS bucket name"
  type        = string
  default     = null
}

variable "lifecycle_rule" {
  description = "GCS bucket lifecycle rule"
  type = object({
    condition = object({
      age = number
    })
    action = object({
      type          = string
      storage_class = string
    })
  })
  default = {
    condition = {
      age = 7
    }
    action = {
      type          = "SetStorageClass"
      storage_class = "COLDLINE"
    }
  }
}

#
# Pub/Sub
#
variable "topic" {
  description = "Cloud Pub/Sub topic name for GCS notification"
  type        = string
  default     = "dbt-artifacts-gcs-notification"
}

#
# BigQuery
#
variable "bigquery_dataset_id" {
  description = "The dataset ID to store dbt artifacts"
  type        = string
  default     = "dbt_artifacts"
}

#
# Cloud Run
#
variable "docker_image" {
  description = "The docker image which runs on Cloud Run"
  type        = string
}
