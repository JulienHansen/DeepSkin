# 📡 DeepSkin API

    This document provides a complete overview of what you can do with our API, as well as its interface. We dockerized our API and made it publicly available on GCloud Run! The source code of our API can be found in the main.py file.

## 🤖 Deployment

### 🐋 Docker

    See Dockerfile for the dockerization of our API.

### ☁️ Cloud

    We decided to host our API on a GCloud Run and to make it publicly available. You can access the API interface on .

## 📡 API Backend

### Overview

    The DeepSkin API is a Flask-based web service that allows users to predict skin conditions from uploaded images using a pre-trained deep learning model. The model is hosted on Google Cloud Storage (GCS) and automatically downloaded when the API starts.

### Features

    Accepts JPG/PNG images as input.

    Includes age, sex, and localization metadata to enhance prediction accuracy.

    Uses a deep learning model stored in GCS to classify skin conditions.

    Returns a JSON response with the predicted class and associated probabilities.

    Includes a simple web interface for testing the API.

### Endpoints

POST /predict

    Description:Processes an image and returns a prediction.

    Request:

    image (file, required): A JPG or PNG image of the skin condition.

    age (string, optional): Patient’s age.

    sex (string, optional): Patient’s gender.

    localization (string, optional): Location of the skin condition on the body.

    Response:
```json
{
    "prediction": "melanoma",
    "probabilities": {
        "melanoma": 0.85,
        "benign_lesion": 0.10,
        "other": 0.05
    },
    "metadata": {
        "age": "45",
        "sex": "male",
        "localization": "back"
    }
}
```

GET /

    Description:Renders a simple HTML interface to upload images for testing.

## Setup & Deployment

### Prerequisites

Python 3.x

Flask

Google Cloud SDK configured with access to the model bucket

### Installation

```bash
pip install -r requirements.txt
```

### Run the API

```bash
python main.py
```

### Notes

The API downloads the model (final_model.pt) from Google Cloud Storage on startup.

Uploaded images are temporarily saved in the static/ directory for debugging.

Logging is enabled to help diagnose issues with image uploads.

