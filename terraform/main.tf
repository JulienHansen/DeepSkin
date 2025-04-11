resource "google_storage_bucket" "dataset_bucket" {
  name     = var.dataset_bucket_name
  location = var.region
}

resource "google_storage_bucket" "model_bucket" {
  name     = var.model_bucket_name
  location = var.region
}

resource "google_storage_bucket" "code_bucket" {
  name     = var.code_bucket_name
  location = var.region
}

resource "google_cloud_run_service" "streamlit_app" {
  name     = "deepskin-app"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/streamlit-app:latest"
        env {
          name  = "MODEL_BUCKET"
          value = var.model_bucket_name
        }
      }
    }
  }

  traffics {
    percent         = 100
    latest_revision = true
  }
}
