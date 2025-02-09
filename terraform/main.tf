locals {
  project        = "my-projects-306716"
  default_region = "asia-east1"
}

provider "google" {
  project = local.project
  region  = local.default_region
}

data "google_project" "default" {}

data "google_service_account" "default" {
  account_id = "cloud-run-default"
}

resource "google_cloud_run_v2_job" "default" {
  name                = "autocomeback"
  location            = local.default_region
  deletion_protection = false

  lifecycle {
    ignore_changes = [client, client_version]
  }

  template {
    parallelism = 1
    task_count  = 1

    template {
      service_account = data.google_service_account.default.email
      max_retries     = 0
      timeout         = "300s"

      containers {
        name  = "api"
        image = "${local.default_region}-docker.pkg.dev/${data.google_project.default.project_id}/ghcr/kvdomingo/autocomeback:latest"

        resources {
          limits = {
            cpu    = "1000m"
            memory = "256Mi"
          }
        }
      }
    }
  }
}
