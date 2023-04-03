module "dbt_artifacts_loader" {
  source = "../module"

  project_id = var.project_id
  region     = var.region

  delete_on_destroy = true

  docker_image = "gcr.io/${var.project_id}/dbt-artifacts-loader:v1.7.0-dev1"

  labels = {
    app = "dbt-artifacts-loader"
  }
}
