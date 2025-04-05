"""
This file contains the main Flask application code for the DeepSkin project.
It includes :
- The download of the model from Google Cloud Storage.
- An API for predicting classes from images and metadata.
- A simple user interface to test the API.
Usage:
    Run this script to start the Flask server.
"""
import logging
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from google.cloud import storage
from PIL import Image
from models.predict import load_model, predict

# Configuration for the API and GCS
HOST = "0.0.0.0"
PORT = 80

# GCS configuration for the trained model
MODEL_BUCKET_URI = "gs://trained_deepskin_model"
MODEL_BLOB_NAME = "final_model.pt"
LOCAL_MODEL_PATH = "final_model.pt"

# Initialize Flask App
app = Flask(__name__)

def download_model_from_gcs(bucket_uri, model_blob_name, local_path):
    """
    Downloads a model from a Google Cloud Storage (GCS) bucket and saves it locally.

    Args:
        bucket_uri (str): The URI of the GCS bucket (for example, ‘gs://my_bucket’).
        model_blob_name (str): The name of the blob (file) in the bucket.
        local_path (str): The local path where the file will be saved.

    Returns:
        None
    """
    bucket_name = bucket_uri.replace("gs://", "")
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(model_blob_name)
    blob.download_to_filename(local_path)
    print(f"Downloaded model from {bucket_uri}/{model_blob_name} to {local_path}")

# Download the trained model and load it
download_model_from_gcs(MODEL_BUCKET_URI, MODEL_BLOB_NAME, LOCAL_MODEL_PATH)
model = load_model(LOCAL_MODEL_PATH)

# Ensure the static directory exists
static_dir = os.path.join(os.getcwd(), 'static')
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

@app.route("/predict", methods=["POST"])
def predict_endpoint():
    """
    Endpoint to make a prediction from an image and metadata.

    This function receives a POST request containing an image and metadata 
    (age, gender, location). It performs the following steps:
    - Checks the presence and format of the image.
    - Validates the image to ensure it is correct.
    - Reads the metadata provided in the request.
    - Calls the prediction function with the image and metadata.
    - Returns the results of the prediction as JSON.

    Returns:
        Response: A JSON response containing :
            - The class predicted with the highest probability.
            - The probabilities for each class.
            - The metadata provided.
        In the event of an error, returns an error message with an appropriate HTTP code.
    """
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400
    age = request.form.get("age")
    sex = request.form.get("sex")

    # Extract the image file
    image_file = request.files["image"]
    # Save the image temporarily for debugging
    temp_image_path = os.path.join(static_dir, 'temp_uploaded_image.jpg')
    image_file.save(temp_image_path)

    # Log image details for debugging
    logging.debug("Image filename: %s", image_file.filename)
    logging.debug("Image content type: %s", image_file.content_type)

    # Check if the content type is valid
    if image_file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        logging.error("Unsupported image format: %s", image_file.content_type)
        return jsonify({"error": "Unsupported image format. Please upload a JPG or PNG file."}), 400

    try:
        # Try opening the image and verify if it's a valid image
        image = Image.open(temp_image_path)  # Use the saved image path here
        image.verify()  # This will check if the image is valid
        image = Image.open(temp_image_path)  # Re-read it after verify() for further processing
    except (IOError, SyntaxError) as error:
        logging.error("Image is invalid: %s", error)
        return jsonify({"error": "Invalid image file"}), 400

    # Rewind the file pointer again for further usage
    image_file.seek(0)
    # Read the image as bytes for further processing
    image_bytes = image_file.read()

    # Extract metadata from the form
    age = request.form.get("age")
    sex = request.form.get("sex")

    localization = request.form.get("localization")

    # Convert metadata to a tuple
    metadata = (age, sex, localization)

    # Call the predict function, passing the image and metadata tuple
    prediction = predict(model, image_bytes, metadata)  # Pass metadata as a tuple

    # Save the image to display on the result page
    image_file.seek(0)  # Rewind the file pointer before saving
    image_file.save(os.path.join(static_dir, 'uploaded_image.jpg'))  # Save the image temporarily

    return jsonify({
        "prediction": max(prediction, key=prediction.get),  # Classe avec la plus grande proba
        "probabilities": prediction,
        "metadata": {
            "age": age,
            "sex": sex,
            "localization": localization
        }
    })

# Simple frontend to test the API
@app.route("/", methods=["GET", "POST"])
def submit():
    """
    Home page for testing the API.

    This function handles GET and POST requests for the welcome page:
    - In the event of a GET request, it displays an HTML page (welcome.html) for submitting a form.
    - In the event of a POST request (form submission), it redirects to the prediction endpoint.

    Returns:
        Response: An HTML page for GET requests or a redirection to the prediction endpoint 
        for POST requests.
    """
    if request.method == "POST":
        # Form submitted, call the predict endpoint
        return redirect(url_for('predict_endpoint'))
    return render_template("welcome.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5100)
    