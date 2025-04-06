"""
This script contains a test function to validate the /predict endpoint of the DeepSkin backend API.

The test sends a POST request to the backend with:
- An image file representing a skin lesion.
- Metadata including age, sex, and localization.

The script verifies the response from the backend and prints:
- The predicted class with the highest probability.
- The probabilities for each class.
- Any error messages if the request fails.
"""

import os
import requests

BACKEND_URL = os.getenv("BACKEND_URL")

def test_backend_route():
    """
    Test the /predict endpoint of the DeepSkin backend API.
    """
    image = "./.github/pictures/test_api.jpg"

    with open(image, 'rb') as file:
        files = {"image": (os.path.basename(image), file, "image/jpeg")}

        data = {
            "age": 35,
            "sex": "male",
            "localization": "scalp"
        }

        response = requests.post(f"{BACKEND_URL}/predict", data=data, files=files, timeout = 10)

        if response.status_code == 200:
            print("Réponse reçue :", response.json())
        else:
            print(f"Erreur: {response.status_code} - {response.text}")

test_backend_route()
