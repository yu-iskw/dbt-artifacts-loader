resource "google_cloud_run_service" "dbt_artifact_loader" {
  project = var.project_id

  name     = "dbt-artifacts-loader"
  location = var.region

  template {
    spec {
      containers {
        image = var.docker_image

        env {
          name  = "ENV_FILE"
          value = ".env/.env.prod"
        }
        env {
          name  = "DESTINATION_PROJECT"
          value = var.project_id
        }
        env {
          name  = "DESTINATION_DATASET"
          value = google_bigquery_dataset.dbt_artifacts.dataset_id
        }
      }

      service_account_name = google_service_account.dbt_artifacts_loader_cloud_run.email
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [google_project_service.run]
}

resource "google_cloud_run_service_iam_member" "cloud_run_invoker" {
  project = var.project_id

  location = google_cloud_run_service.dbt_artifact_loader.location
  service  = google_cloud_run_service.dbt_artifact_loader.name
  role     = "roles/run.invoker"
  member   = "serviceAccount:${google_service_account.cloud_run_invoker.email}"
}
