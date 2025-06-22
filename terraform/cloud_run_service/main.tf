terraform {
  required_version = ">= 1.0"
  backend "gcs" {
    bucket = ""                                                               # Replace with your GCS bucket name
    prefix = "terraform/state/template-python-devcontainer-cloud-run-service" # Replace with your desired prefix
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Service Account
data "google_service_account" "default" {
  account_id = var.service_account_id
  project    = var.project_id
}

data "google_artifact_registry_repository" "my_repo" {
  project       = var.project_id
  location      = var.region
  repository_id = var.repo_name
}


resource "google_cloud_run_v2_service" "default" {
  name                = var.service_name
  location            = var.region
  project             = var.project_id
  ingress             = "INGRESS_TRAFFIC_ALL"
  deletion_protection = false


  template {
    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.my_repo.repository_id}/${var.image_name}:${var.image_tag}"
      ports {
        container_port = 8080
      }
      resources {
        limits = {
          cpu    = "1"
          memory = "512Mi"
        }
      }

    }

    service_account = google_service_account.default.email

  }
}

resource "google_cloud_run_v2_service_iam_member" "public_access" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.default.name
  role     = "roles/run.invoker"
  member   = "allUsers"
  # member = "allAuthenticatedUsers"
}
