variable "project_id" {
  type        = string
  description = "GCP Project ID"
}

variable "region" {
  type        = string
  default     = "europe-west1"
  description = "GCP Region"
}

variable "dataset_bucket_name" {
  type        = string
  default     = "deepskin-dataset-bucket"
}

variable "model_bucket_name" {
  type        = string
  default     = "deepskin-model-bucket"
}

variable "code_bucket_name" {
  type        = string
  default     = "deepskin-code-bucket"
}
