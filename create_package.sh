#!/bin/bash

# Define your bucket name and package details
BUCKET_NAME="deepskin_code"
PACKAGE_PATH="./dist/deepskin_vertex-0.1.tar.gz"
GCS_DEST_PATH="gs://$BUCKET_NAME/pytorch-on-gcp//train/python_package/deepskin_vertex-0.1.tar.gz"

# Check if the bucket exists
if ! gsutil ls -b gs://$BUCKET_NAME &>/dev/null; then
  echo "Bucket gs://$BUCKET_NAME does not exist. Creating..."
  # Create the bucket in the desired location (e.g., US)
  gsutil mb -l US gs://$BUCKET_NAME
else
  echo "Bucket gs://$BUCKET_NAME already exists."
fi

# Upload the package to GCS
gsutil cp $PACKAGE_PATH $GCS_DEST_PATH
