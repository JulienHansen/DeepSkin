"""

"""

import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL")

import requests

def test_backend_route():
    image = "./.github/pictures/test_api.jpg"
    
    with open(image, 'rb') as file:
        files = {"image": (os.path.basename(image), file, "image/jpeg")}
        
        data = {
            "age": 35,
            "sex": "male",
            "localization": "scalp"
        }

        response = requests.post(f"{BACKEND_URL}/predict", data=data, files=files)
        
        if response.status_code == 200:
            print("Réponse reçue :", response.json()) 
        else:
            print(f"Erreur: {response.status_code} - {response.text}")
            
test_backend_route()
