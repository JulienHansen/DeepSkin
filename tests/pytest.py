"""

"""

import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL")

def test_backend_route():
    assert BACKEND_URL is not None
    print(BACKEND_URL)
    response = requests.get(f"{BACKEND_URL}/") 
    assert response.status_code == 200