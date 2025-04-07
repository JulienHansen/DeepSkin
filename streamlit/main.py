"""
This Streamlit application provides an interface for the DeepSkin project.

It includes:
- A "Prediction" page for uploading skin lesion images, entering metadata (age, sex, localization),
  and receiving predictions from a backend API.
- A "Dashboard" page for monitoring Cloud Run metrics such as CPU usage, RAM usage, request count,
  and request latency.

Key Features:
- Displays detailed probabilities for each skin lesion class with progress bars.
- Provides diagnostic information for each skin lesion class.
- Monitors Cloud Run metrics in real-time using Google Cloud Monitoring.

Usage:
    Run this script to launch the Streamlit application:
    streamlit run streamlit.py
"""

# pylint: disable=no-member
import time
import datetime
import os
from google.cloud import monitoring_v3
import pandas as pd
import requests
import streamlit as st
import pytz

client = monitoring_v3.MetricServiceClient()
PROJECT_NAME = "projects/deepskin-451908"

HIDE_STREAMLIT_STYLE = """
<style>
#MainMenu {visibility: hidden;}
.stDeployButton {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""


st.markdown(HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5100")

PAGES = {
    "Prediction": "prediction",
    "Dashboard": "dashboard",
}

def get_metrics(metric_filter: str, metric_label: str, input_interval_seconds: int):
    """
    Retrieve metrics from Google Cloud Monitoring for a specified time interval.

    This function queries Google Cloud Monitoring for metrics such as CPU usage, RAM usage,
    request count, or request latency, and returns the metric values and their corresponding 
    timestamps.

    Args:
        metric_filter (str): The filter string to specify the metric type and resource type.
        metric_label (str): A label describing the metric (e.g., "CPU", "RAM", "Request Count").
        interval_seconds (int): The time interval in seconds for which to retrieve metrics.

    Returns:
        tuple: A tuple containing:
            - usage_percent (list): A list of metric values (e.g., CPU usage percentage).
            - times (list): A list of timestamps corresponding to the metric values.
    """
    interval = monitoring_v3.TimeInterval(
        start_time={"seconds": int(time.time()) - input_interval_seconds},
        end_time={"seconds": int(time.time())}
    )

    request = monitoring_v3.ListTimeSeriesRequest(
        name=PROJECT_NAME,
        filter=metric_filter,
        interval=interval,
    )

    time_series = client.list_time_series(request)

    times = []
    usage_percent = []
    for series in time_series:
        for point in series.points:
            timestamp = point.interval.end_time
            metric_value = None

            if metric_label in {"CPU", "RAM", "Request Latency"}:
                start_time = point.interval.start_time

                mean = point.value.distribution_value.mean
                if metric_label == "Request Latency":
                    usage_percent_value = mean / 1000
                else:
                    usage_percent_value = mean * 100

                times.append(start_time)
                usage_percent.append(usage_percent_value)

            if metric_label == "Request Count":
                timestamp = point.interval.end_time
                metric_value = point.value.int64_value
                times.append(timestamp)
                usage_percent.append(metric_value)

    return usage_percent, times

st.sidebar.image("./.github/pictures/logo-bg.png",use_container_width=True)
page = st.sidebar.selectbox("Choose a page", options=list(PAGES.keys()))


if page == "Prediction":

    st.markdown("""
        <style>
        .custom-header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: #0e1117; /* Couleur du fond (tu peux la changer) */
            color: white;
            text-align: center;
            padding: 10px;
            font-size: 24px;
            z-index: 9999;
            border-bottom: 1px solid #444;
        }

        /* Ajoute un padding pour éviter que le header recouvre le contenu */
        .main > div {
            padding-top: 80px; /* Ajuste selon la hauteur de ton header */
        }
        </style>

        <div class="custom-header">
            🔬 DeepSkin - Analyse d'images de la peau avec IA
        </div>
    """, unsafe_allow_html=True)

    header = st.container()
    header.title("Skin analysis with AI 🔬")
    header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

    st.markdown(
        """
    <style>
        div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
            position: sticky;
            top: 2.875rem;
            background-color: white;
            z-index: 999;
        }
        .fixed-header {
            border-bottom: 1px solid black;
        }
    </style>
        """,
        unsafe_allow_html=True
    )


    diagnosis_info = {
        "akiec": {
            "name": "Actinic Keratoses / Bowen's Disease",
            "description": "Precancerous skin lesions often caused by sun damage. "
                            "Can develop into squamous cell carcinoma."
        },
        "bcc": {
            "name": "Basal Cell Carcinoma",
            "description": "The most common type of skin cancer, usually "
                            "localized and slow-growing."
        },
        "bkl": {
            "name": "Benign Keratosis-like Lesions",
            "description": "Non-cancerous growths like solar lentigines, "
                            "seborrheic keratoses, and lichen-planus like keratoses."
        },
        "df": {
            "name": "Dermatofibroma",
            "description": "Benign skin nodule, often firm and small, typically not harmful."
        },
        "mel": {
            "name": "Melanoma",
            "description": "A serious form of skin cancer that can spread quickly if not "
                            "treated early."
        },
        "nv": {
            "name": "Melanocytic Nevi",
            "description": "Common moles made up of pigment-producing cells; generally harmless."
        },
        "vasc": {
            "name": "Vascular Lesions",
            "description": "Includes angiomas, angiokeratomas, pyogenic granulomas, "
                            "and hemorrhage. Usually benign."
        },
    }

    with st.expander("Details of all possible diagnoses"):
        for key, value in diagnosis_info.items():
            st.write(f"### {value['name']}")
            st.write(value["description"])
            st.write("---")

    # API URL
    API_URL = f"{BACKEND_URL}/predict"

    #st.title("Skin analysis with AI")

    age = st.number_input("Age", min_value=0, max_value=120)
    sex = st.selectbox("Sexe", ["male", "female"])
    localizations = [
        'scalp', 'ear', 'face', 'back', 'trunk', 'chest', 'upper extremity', 'abdomen',
        'unknown', 'lower extremity', 'genital', 'neck', 'hand', 'foot', 'acral'
    ]
    localization = st.selectbox("Localization", localizations)

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if st.button("Analyze the image"):
        if uploaded_file is not None:
            files = {"image": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            data = {"age": age, "sex": sex, "localization": localization}
            headers = {"Accept": "application/json"}

            response = requests.post(API_URL, files=files, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                result = response.json()
                st.image(uploaded_file, caption="Uploaded image", use_container_width=True)
                st.write("### Analysis Result")
                st.write(f"**Predicted class :** {result['prediction']}")

                #st.write("#### Détails des probabilités")
                #st.json(result.get("probabilities", {}))

                probabilities = result.get("probabilities", {})
                # Conversion en DataFrame
                df = pd.DataFrame(list(probabilities.items()), columns=["Nom de la maladie",
                                                                        "Probabilité"])

                # Affichage du titre
                st.write("#### Details of probabilities")

                # Affichage du tableau avec les barres de progression
                for index, row in df.iterrows():
                    col1, col2, col3 = st.columns([2, 3, 1])

                    with col1:
                        st.write(row["Nom de la maladie"])

                    with col2:
                        st.progress(row["Probabilité"])  # Affiche une barre de progression

                    with col3:
                        # Affiche le pourcentage en chiffres
                        st.write(f"{row['Probabilité']*100:.6f}%")
            else:
                st.error(f"Error: {response.json().get('error', 'Uknown error')}")
        else:
            st.warning("Please upload an image before analyzing.")


elif page == "Dashboard":

    header = st.container()
    header.title("Monitoring Cloud Run metrics 🖥️")
    header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

    st.markdown(
        """
    <style>
        div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
            position: sticky;
            top: 2.875rem;
            background-color: white;
            z-index: 999;
        }
        .fixed-header {
            border-bottom: 1px solid black;
        }
    </style>
        """,
        unsafe_allow_html=True
    )

    #st.title("Monitoring Cloud Run metrics")

    interval_choice = st.selectbox(
    "Choose the time interval",
    ["24 heures", "1 heure", "5 minutes"]
    )

    if interval_choice == "24 heures":
        INTERVAL_SECONDS = 86400  # 24 heures en secondes
    elif interval_choice == "1 heure":
        INTERVAL_SECONDS = 3600  # 1 heure en secondes
    else:
        INTERVAL_SECONDS = 300  # 5 minutes en secondes

    MATRIC_LABEL_CPU = "CPU"
    MATRIC_LABEL_RAM = "RAM"
    METRIC_LABEL_REQUEST_COUNT = "Request Count"
    MATRIC_LABEL_REQUEST_LATENCY = "Request Latency"

    CPU_METRIC_FILTER = 'metric.type="run.googleapis.com/container/cpu/utilizations" ' \
                        'AND resource.type="cloud_run_revision"'
    RAM_METRIC_FILTER = 'metric.type="run.googleapis.com/container/memory/utilizations" ' \
                        'AND resource.type="cloud_run_revision"'
    REQUEST_COUNT_METRIC_FILTER = 'metric.type="run.googleapis.com/request_count" ' \
                                    'AND resource.type="cloud_run_revision"'
    REQUEST_LATENCY_METRIC_FILTER = 'metric.type="run.googleapis.com/request_latencies" ' \
                                    'AND resource.type="cloud_run_revision"'

    tab1, tab2, tab3, tab4 = st.tabs(["CPU", "RAM", "Request Count", "Request Latency"])

    brussels_tz = pytz.timezone("Europe/Brussels")

    with tab1:
        usage_percent_cpu, times_cpu = get_metrics(CPU_METRIC_FILTER, MATRIC_LABEL_CPU,
                                                   INTERVAL_SECONDS)
        times_cpu = [datetime.datetime.fromtimestamp(time.timestamp(), brussels_tz) for time in times_cpu]
        df_cpu = pd.DataFrame({"Time": times_cpu, "CPU Usage (%)": usage_percent_cpu})
        st.line_chart(df_cpu.set_index("Time"), height=250)
        st.write(df_cpu)

    with tab2:
        usage_percent_ram, times_ram = get_metrics(RAM_METRIC_FILTER, MATRIC_LABEL_RAM,
                                                   INTERVAL_SECONDS)
        times_ram = [datetime.datetime.fromtimestamp(time.timestamp(), brussels_tz) for time in times_ram]
        df_ram = pd.DataFrame({"Time": times_ram, "RAM Usage (%)": usage_percent_ram})
        st.line_chart(df_ram.set_index("Time"), height=250)
        st.write(df_ram)

    with tab3:
        usage_percent_request_count, times_request_count = get_metrics(REQUEST_COUNT_METRIC_FILTER,
                                                METRIC_LABEL_REQUEST_COUNT, INTERVAL_SECONDS)
        times_request_count = [datetime.datetime.fromtimestamp(time.timestamp(), brussels_tz) for time in times_request_count]
        df_request_count = pd.DataFrame({"Time": times_request_count, "Request Count":
                                         usage_percent_request_count})
        st.line_chart(df_request_count.set_index("Time"), height=250)
        st.write(df_request_count)

    with tab4:
        usage_percent_request_latency, times_request_latency = get_metrics(
            REQUEST_LATENCY_METRIC_FILTER, MATRIC_LABEL_REQUEST_LATENCY, INTERVAL_SECONDS)
        times_request_latency = [datetime.datetime.fromtimestamp(time.timestamp(), brussels_tz) for time in times_request_latency]
        df_request_latency = pd.DataFrame({"Time": times_request_latency, "Request Latency (ms)":
                                           usage_percent_request_latency})
        st.line_chart(df_request_latency.set_index("Time"), height=250)
        st.write(df_request_latency)
