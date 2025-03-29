from flask import Flask, render_template, request, jsonify, redirect, url_for
from models.predict import load_model, predict
from google.cloud import storage
import os
from PIL import Image
import io

# Configuration for the API and GCS
HOST = "0.0.0.0"
PORT = 80

# GCS configuration for the trained model
MODEL_BUCKET_URI = "gs://trained_deepskin_model"
MODEL_BLOB_NAME = "final_model.pt"
LOCAL_MODEL_PATH = "final_model.pt"

# Initialize Flask App
app = Flask(__name__)

# Function to download the model from GCS
def download_model_from_gcs(bucket_uri, model_blob_name, local_path):
    bucket_name = bucket_uri.replace("gs://", "")
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(model_blob_name)
    blob.download_to_filename(local_path)
    print(f"Downloaded model from {bucket_uri}/{model_blob_name} to {local_path}")

# Download the trained model and load it
download_model_from_gcs(MODEL_BUCKET_URI, MODEL_BLOB_NAME, LOCAL_MODEL_PATH)
model = load_model(LOCAL_MODEL_PATH)

import logging

# Ensure the static directory exists
static_dir = os.path.join(os.getcwd(), 'static')
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

@app.route("/predict", methods=["POST"])
def predict_endpoint():
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
    logging.debug(f"Image filename: {image_file.filename}")
    logging.debug(f"Image content type: {image_file.content_type}")
    
    # Check if the content type is valid
    if image_file.content_type not in ["image/jpeg", "image/png", "image/jpg"]:
        logging.error(f"Unsupported image format: {image_file.content_type}")
        return jsonify({"error": "Unsupported image format. Please upload a JPG or PNG file."}), 400

    try:
        # Try opening the image and verify if it's a valid image
        image = Image.open(temp_image_path)  # Use the saved image path here
        image.verify()  # This will check if the image is valid
        image = Image.open(temp_image_path)  # Re-read it after verify() for further processing
    except (IOError, SyntaxError) as e:
        logging.error(f"Image is invalid: {e}")
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

    return render_template(
        'result.html',
        prediction=prediction,
        image_url='/static/uploaded_image.jpg',
        age=age,
        sex=sex,
        localization=localization
    )


# Simple frontend to test the API
@app.route("/", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        # Form submitted, call the predict endpoint
        return redirect(url_for('predict_endpoint'))
    
    return render_template("welcome.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5100)
