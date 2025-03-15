from google.cloud import aiplatform
from datetime import datetime

# --- CONFIG ---
PRE_BUILT_TRAINING_CONTAINER_IMAGE_URI = "europe-docker.pkg.dev/vertex-ai/training/pytorch-gpu.1-13.py310:latest"

APP_NAME = "deep_skin"
PROJECT_ID = "deepskin-451908"  
BUCKET_URI = "gs://deepskin_code" 
LOCATION = "europe-west1"



PYTHON_PACKAGE_APPLICATION_DIR = ".."
source_package_file_name = f"{PYTHON_PACKAGE_APPLICATION_DIR}/dist/deepskin_vertex-0.1.tar.gz"
python_package_gcs_uri = f"{BUCKET_URI}/pytorch-on-gcp//train/python_package/deepskin_vertex-0.1.tar.gz"
python_module_name = "models.train" 

# Initialize Vertex SDK
aiplatform.init(project=PROJECT_ID, staging_bucket=BUCKET_URI)

TIMESTAMP = datetime.now().strftime("%Y%m%d%H%M%S")
JOB_NAME = f"{APP_NAME}-training-{TIMESTAMP}"

print(f"Starting training job: {JOB_NAME}")
print(f"Using container: {PRE_BUILT_TRAINING_CONTAINER_IMAGE_URI}")
print(f"Python package GCS URI: {python_package_gcs_uri}")

# Create a Custom Training Job
job = aiplatform.CustomPythonPackageTrainingJob(
    display_name=JOB_NAME,
    python_package_gcs_uri=python_package_gcs_uri,
    python_module_name=python_module_name,
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
