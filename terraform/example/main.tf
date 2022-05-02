module "dbt_artifacts_loader" {
  source = "../module"

  project_id = var.project_id
  region     = var.region

  delete_on_destroy = true

  docker_image = "gcr.io/${var.project_id}/dbt-artifacts-loader:v1.3.0-dev3"

  labels = {
    app = "dbt-artifacts-loader"
  }
}
