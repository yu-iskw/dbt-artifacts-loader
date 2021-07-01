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
  default     = "asia-northeast1"
}
