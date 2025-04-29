from locust import HttpUser, task, between
import os

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)

    @task#(2)
    def test_predict_endpoint(self):
        image = "./.github/pictures/test_api.jpg"

        with open(image, 'rb') as file:
            files = {"image": (os.path.basename(image), file, "image/jpeg")}

            data = {
                "age": 35,
                "sex": "male",
                "localization": "scalp"
            }

            response = self.client.post("/predict", data=data, files=files)

            if response.status_code == 200:
                print("Prediction receive:", response.json())
            else:
                print(f"Prediction failed: {response.status_code} - {response.text}")

    #@task(1)
    #def test_frontend(self):
    #    response = self.client.get("/")
    #    if response.status_code == 200:
    #        print("Frontend is accessible")
    #    else:
    #        print("Failed to access frontend:", response.status_code)
