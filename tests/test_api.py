"""

"""

import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "https://deepskin-back-ster3eab3q-ew.a.run.app")

def test_backend_route():
    assert BACKEND_URL is not None, "Backend URL is not defined"
    print(BACKEND_URL)
    response = requests.get(f"{BACKEND_URL}/") 
    assert response.status_code == 200