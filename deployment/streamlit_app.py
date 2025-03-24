import streamlit as st
import requests
import io
from PIL import Image

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
