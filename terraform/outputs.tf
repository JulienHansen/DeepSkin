output "streamlit_url" {
  value = google_cloud_run_service.streamlit_app.status[0].url
}

output "model_bucket" {
  value = google_storage_bucket.model_bucket.url
}
