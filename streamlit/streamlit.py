import streamlit as st 
import requests

from google.cloud import monitoring_v3
import time
import datetime
import pandas as pd
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5100")

PAGES = {
    "Prediction": "prediction",
    "Dashboard": "dashboard",
}

def get_metrics(metric_filter: str, metric_label: str, interval_seconds: int):
    interval = monitoring_v3.TimeInterval(
        start_time={"seconds": int(time.time()) - interval_seconds},
        end_time={"seconds": int(time.time())}
    )
    
    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=metric_filter,
        interval=interval,
    )

    time_series = client.list_time_series(request)

    times = []
    usage_percent = []
    for series in time_series:
        for point in series.points:
            timestamp = point.interval.end_time
            value = None

            if(metric_label == "CPU" or metric_label == "RAM" or metric_label == "Request Latency"):
                start_time = point.interval.start_time
                end_time = point.interval.end_time

                start_seconds = start_time.timestamp() 
                end_seconds = end_time.timestamp()

                duration = end_seconds - start_seconds

                mean = point.value.distribution_value.mean
                if(metric_label == "Request Latency"):
                    usage_percent_value = mean / 1000
                else:
                    usage_percent_value = mean * 100

                times.append(start_time)
                usage_percent.append(usage_percent_value)

            if(metric_label == "Request Count"):
                timestamp = point.interval.end_time
                value = point.value.int64_value 
                times.append(timestamp)
                usage_percent.append(value)

    return usage_percent, times


page = st.sidebar.selectbox("Choisissez une page", options=list(PAGES.keys()))

if page == "Prediction":

    diagnosis_info = {
        "akiec": {
            "name": "Actinic Keratoses / Bowen's Disease",
            "description": "Precancerous skin lesions often caused by sun damage. Can develop into squamous cell carcinoma."
        },
        "bcc": {
            "name": "Basal Cell Carcinoma",
            "description": "The most common type of skin cancer, usually localized and slow-growing."
        },
        "bkl": {
            "name": "Benign Keratosis-like Lesions",
            "description": "Non-cancerous growths like solar lentigines, seborrheic keratoses, and lichen-planus like keratoses."
        },
        "df": {
            "name": "Dermatofibroma",
            "description": "Benign skin nodule, often firm and small, typically not harmful."
        },
        "mel": {
            "name": "Melanoma",
            "description": "A serious form of skin cancer that can spread quickly if not treated early."
        },
        "nv": {
            "name": "Melanocytic Nevi",
            "description": "Common moles made up of pigment-producing cells; generally harmless."
        },
        "vasc": {
            "name": "Vascular Lesions",
            "description": "Includes angiomas, angiokeratomas, pyogenic granulomas, and hemorrhage. Usually benign."
        },
    }

    with st.expander("Détails de tous les diagnostics possibles"):
        for key, value in diagnosis_info.items():
            st.write(f"### {value['name']}")
            st.write(value["description"])
            st.write("---") 

    # API URL
    API_URL = "http://localhost:5100/predict"
    API_URL = f"{BACKEND_URL}/predict"
    print(API_URL)

    st.title("Analyse de la peau avec IA")

    age = st.number_input("Âge", min_value=0, max_value=120)
    sex = st.selectbox("Sexe", ["male", "female"])
    localizations = [
        'scalp', 'ear', 'face', 'back', 'trunk', 'chest', 'upper extremity', 'abdomen',
        'unknown', 'lower extremity', 'genital', 'neck', 'hand', 'foot', 'acral'
    ]
    localization = st.selectbox("Localisation", localizations)

    uploaded_file = st.file_uploader("Téléchargez une image", type=["jpg", "jpeg", "png"])

    if st.button("Analyser l'image"):
        if uploaded_file is not None:
            files = {"image": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            data = {"age": age, "sex": sex, "localization": localization}
            headers = {"Accept": "application/json"}

            response = requests.post(API_URL, files=files, data=data, headers=headers)

            if response.status_code == 200:
                result = response.json()
                st.image(uploaded_file, caption="Image téléchargée", use_container_width=True)
                st.write("### Résultat de l'analyse")
                st.write(f"**Classe prédite :** {result['prediction']}")
                
                st.write("#### Détails des probabilités")
                st.json(result.get("probabilities", {}))
            else:
                st.error(f"Erreur: {response.json().get('error', 'Erreur inconnue')}")
        else:
            st.warning("Veuillez télécharger une image avant d'analyser.")


elif page == "Dashboard":
    client = monitoring_v3.MetricServiceClient()
    project_name = "projects/deepskin-451908" 

    st.title("Monitoring des métriques Cloud Run")

    interval_choice = st.selectbox(
    "Choisir l'intervalle de temps",
    ["24 heures", "1 heure", "5 minutes"]
    )

    if interval_choice == "24 heures":
        interval_seconds = 86400  # 24 heures en secondes
    elif interval_choice == "1 heure":
        interval_seconds = 3600  # 1 heure en secondes
    else:
        interval_seconds = 300  # 5 minutes en secondes

    metric_label = st.selectbox(
    "Choisir la métrique",
    ["CPU", "RAM", "Request Count", "Request Latency"]
    )


    metric_label_cpu = "CPU"
    metric_label_ram = "RAM"
    metric_label_request_count = "Request Count"
    metric_label_request_latency = "Request Latency"

    cpu_metric_filter = 'metric.type="run.googleapis.com/container/cpu/utilizations" AND resource.type="cloud_run_revision"'
    ram_metric_filter = 'metric.type="run.googleapis.com/container/memory/utilizations" AND resource.type="cloud_run_revision"'
    request_count_metric_filter = 'metric.type="run.googleapis.com/request_count" AND resource.type="cloud_run_revision"'
    request_latency_metric_filter = 'metric.type="run.googleapis.com/request_latencies" AND resource.type="cloud_run_revision"'   

    tab1, tab2, tab3, tab4 = st.tabs(["CPU", "RAM", "Request Count", "Request Latency"]) 

    with tab1:
        usage_percent_cpu, times_cpu = get_metrics(cpu_metric_filter, metric_label_cpu, interval_seconds)
        times_cpu = [datetime.datetime.utcfromtimestamp(time.timestamp()) for time in times_cpu]
        df_cpu = pd.DataFrame({"Time": times_cpu, "CPU Usage (%)": usage_percent_cpu})
        st.line_chart(df_cpu.set_index("Time"), height=250)
        st.write(df_cpu)

    with tab2:
        usage_percent_ram, times_ram = get_metrics(ram_metric_filter, metric_label_ram, interval_seconds)
        times_ram = [datetime.datetime.utcfromtimestamp(time.timestamp()) for time in times_ram]
        df_ram = pd.DataFrame({"Time": times_ram, "RAM Usage (%)": usage_percent_ram})
        st.line_chart(df_ram.set_index("Time"), height=250)
        st.write(df_ram)

    with tab3:
        usage_percent_request_count, times_request_count = get_metrics(request_count_metric_filter, metric_label_request_count, interval_seconds)
        times_request_count = [datetime.datetime.utcfromtimestamp(time.timestamp()) for time in times_request_count]
        df_request_count = pd.DataFrame({"Time": times_request_count, "Request Count": usage_percent_request_count})
        st.line_chart(df_request_count.set_index("Time"), height=250)
        st.write(df_request_count)

    with tab4:
        usage_percent_request_latency, times_request_latency = get_metrics(request_latency_metric_filter, metric_label_request_latency, interval_seconds)
        times_request_latency = [datetime.datetime.utcfromtimestamp(time.timestamp()) for time in times_request_latency]
        df_request_latency = pd.DataFrame({"Time": times_request_latency, "Request Latency (ms)": usage_percent_request_latency})
        st.line_chart(df_request_latency.set_index("Time"), height=250)
        st.write(df_request_latency)
