"""
This script configures and submits a custom training job to Google Cloud Vertex AI.

The training job uses a pre-built PyTorch container and a Python package containing the DeepSkin
training code. The script initializes the Vertex AI SDK, defines the training job configuration,
and submits the job to Vertex AI for execution.

Key components:
- Configuration for the Vertex AI training job, including container image, project ID,
    and bucket URI.
- Packaging and uploading the Python training code to Google Cloud Storage (GCS).
- Submitting the training job with specified arguments, such as learning rate, batch size,
    and epochs.

Usage:
    Run this script to submit a training job to Vertex AI:
    python main_vertex.py

Requirements:
- Google Cloud SDK must be installed and authenticated.
- The Python package containing the training code must be built and uploaded to GCS.
- Vertex AI API must be enabled for the Google Cloud project.

"""

from datetime import datetime
from google.cloud import aiplatform


# --- CONFIG ---
PRE_BUILT_TRAINING_CONTAINER_IMAGE_URI = "europe-docker.pkg.dev" \
"/vertex-ai/training/pytorch-gpu.1-13.py310:latest"

APP_NAME = "deep_skin"
PROJECT_ID = "deepskin-451908"
BUCKET_URI = "gs://deepskin_code"
LOCATION = "europe-west1"


PYTHON_PACKAGE_APPLICATION_DIR = ".."
SOURCE_PACKAGE_FILE_NAME = f"{PYTHON_PACKAGE_APPLICATION_DIR}/dist/deepskin_vertex-0.1.tar.gz"
PYTHON_PACKAGE_GCS_URI = f"{BUCKET_URI}/pytorch-on-gcp//train/python_package/" \
"deepskin_vertex-0.1.tar.gz"
PYTHON_MODULE_NAME = "models.train"

# Initialize Vertex SDK
aiplatform.init(project=PROJECT_ID, staging_bucket=BUCKET_URI)

TIMESTAMP = datetime.now().strftime("%Y%m%d%H%M%S")
JOB_NAME = f"{APP_NAME}-training-{TIMESTAMP}"

print(f"Starting training job: {JOB_NAME}")
print(f"Using container: {PRE_BUILT_TRAINING_CONTAINER_IMAGE_URI}")
print(f"Python package GCS URI: {PYTHON_PACKAGE_GCS_URI}")

# Create a Custom Training Job
job = aiplatform.CustomPythonPackageTrainingJob(
    display_name=JOB_NAME,
    python_package_gcs_uri=PYTHON_PACKAGE_GCS_URI,
    python_module_name=PYTHON_MODULE_NAME,
    container_uri=PRE_BUILT_TRAINING_CONTAINER_IMAGE_URI,
    location=LOCATION
)

# Define training arguments
training_args = [
    "--data_path", "models/data",
    "--epochs", "10",
    "--batch_size", "64",
    "--lr", "0.0003",
    "--train_prop", "0.8",
    "--device", "cuda",
    "--img_size", "224",
    "--max_samples", "1000",
    "--optimizer", "AdamW",
    "--save_path", "gs://trained_deepskin_model/trained_models/",
    "--on_cloud",
]

# Submit the Job to Vertex AI
job.run(
    replica_count=1,
    machine_type="n1-standard-8",
    accelerator_type="NVIDIA_TESLA_T4",
    accelerator_count=1,
    args=training_args,
    sync=True,
    service_account="808565425437-compute@developer.gserviceaccount.com"
)
