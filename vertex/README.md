# 🚀 Training in the Cloud with Vertex AI

The code we use to train our model locally can be found in models/train.py. This section details how we configured Vertex AI to make our scripts runnable on Google Cloud.

## 📦 Dependencies

Although it is possible to use a custom Docker image for Vertex AI, we chose not to, as this would require building and uploading a 10GB+ image. Instead, we use a pre-built PyTorch image provided by Vertex AI:

PRE_BUILT_TRAINING_CONTAINER_IMAGE_URI = "europe-docker.pkg.dev/vertex-ai/training/pytorch-gpu.1-13.py310:latest"

## 🏗️ Package Creation

To use Vertex AI, we must package our code as a Python package. This involves:

Creating a setup.py to structure our code as a package.

Writing a bash script (create_package.sh) to:

Upload the package to a Google Cloud Storage (GCS) bucket.

Automatically create the bucket if it does not exist.

Once uploaded, Vertex AI can fetch the package and execute it.

## 📂 Dataset Storage

We store our dataset in Google Cloud Storage (GCS) instead of downloading it manually. This has two benefits:
✅ Faster access when training in Vertex AI.
✅ Scalability for larger datasets.

## 🎯 Training in the Cloud

The script main_vertex.py launches the training job on Vertex AI using the following steps:

Initialize Vertex AI SDK:

aiplatform.init(project=PROJECT_ID, staging_bucket=BUCKET_URI)

Define a custom training job:

```python
job = aiplatform.CustomPythonPackageTrainingJob(
    display_name=JOB_NAME,
    python_package_gcs_uri=python_package_gcs_uri,
    python_module_name=python_module_name,
    container_uri=PRE_BUILT_TRAINING_CONTAINER_IMAGE_URI,
    location=LOCATION
)
```
```python
Submit the job:

job.run(
    replica_count=1,
    machine_type="n1-standard-8",
    accelerator_type="NVIDIA_TESLA_T4",
    accelerator_count=1,
    args=training_args,
    sync=True,
    service_account="808565425437-compute@developer.gserviceaccount.com"
)
```

💾 Model Saving

Once training is complete, the model is stored in a GCS bucket:

```bash
"--save_path", "gs://trained_deepskin_model/trained_models/"
```

This allows us to retrieve and deploy the model easily.

🔄 CI/CD: Automatic Training

To automate training, we integrate CI/CD pipelines that:
✅ Automatically package and upload trained model when the commit message starts with !train_vertex! .
✅ Deploy the latest trained models.