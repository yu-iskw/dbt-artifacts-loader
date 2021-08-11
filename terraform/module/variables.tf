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

variable "bucket_writers" {
  description = "The list of members who can writer to the bucket for dbt artifacts"
  type        = list(string)
  default     = []
}

variable "bucket_readers" {
  description = "The list of members who can access the bucket for dbt artifacts"
  type        = list(string)
  default     = []
}

#
# Pub/Sub
#
variable "pubsub_topic" {
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
