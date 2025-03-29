# DeepSkin - Frontend

## Description
Deepskin is a streamlit application for analysing skin images to detect different classes of skin lesions such as : 

    - Actinic Keratoses / Bowen's Disease (akiec)
    - Basal Cell Carcinoma (bcc)
    - Benign Keratosis-like Lesions (bkl)
    - Dermatofibroma (df)
    - Melanoma (mel)
    - Melanocytic Nevi (nv)
    - Vascular Lesions (vasc)
The application also includes a dashboard for viewing performance metrics (CPU, RAM, number of requests, latency) from Google Cloud Run

## Project structure

```
.
├── streamlit/               # Folder containing the frontend code
│   ├── streamlit.py         # Streamlit user interface
│   ├── requirements.txt     # Python dependency file
│   ├── Dockerfile           # Dockerfile for the Streamlit application
│   └── README.md            # Project documentation
```

## Installation
### Prerequisites 
- Python
- Docker
- Cloud account with API Monitoring enabled

### Configuration
Create an environment file with the following variable:
```
BACKEND_URL=http://localhost:5100
```
It should be noted that if you are running locally there is no need to specify the URL as it is supplied as standard if no other URL is given.
## Launch the application
### Local with streamlit
```
streamlit run streamlit/streamlit.py
```
### With Docker
Building the image: 
```
docker build -t deepskin-front -f Dockerfile .
```

Launch the container: 
```
docker run -p 8501:8501 deepskin-front
```
Access the interface via: http://localhost:8501

## Functionality
### Prediction page
- Choice of age, sex and location of lesion
- Download the type of skin lesion with a detailed explanation
- Display of the image with the analysis result

### Dashboard page
- Selecting a time interval for displaying metrics
- View Cloud Run metrics: 
    - CPU usage
    - RAM usage
    - Number of requests 
    - Request latency
 