# DeepSkin :adhesive_bandage:

## :memo: About the Project

Skin cancer is one of the most common forms of cancer, and early detection is crucial for effective treatment. However, many people worldwide lack easy access to dermatologists, leading to delays in diagnosis and unnecessary medical visits.

**DeepSkin** aims to bridge this gap by providing an AI-powered solution for analyzing skin lesions. Users can upload images of their skin lesions, and our deep learning model will assess whether the lesion is likely to be malignant or benign.

By filtering out benign cases, DeepSkin helps reduce unnecessary dermatology visits while ensuring that high-risk cases receive urgent medical attention. This not only improves patient outcomes but also optimizes healthcare resources by allowing medical professionals to focus on cases that require immediate intervention.

## :bulb: Value Proposition

- **Easy-to-use Interface**: No medical expertise required; users simply upload an image.
- **Risk Assessment**: The model provides a classification and a confidence score.
- **Reduced Unnecessary Visits**: Helps users identify benign cases while ensuring high-risk cases get urgent attention.
- **Cloud-Based Solution**: Accessible anywhere, anytime.

## :stethoscope: Our Team

The DeepSkin Team is composed of 4 members:
- Hansen Julien
- Vermeylen Clément
- Arsanov Ramzan
- Seyfullah Ural

## :dart: Objectives

1. Develop a deep learning model to classify skin lesions with high accuracy.
2. Provide an intuitive and user-friendly web application for users to interact with the model.
3. Ensure the system can scale and be deployed efficiently on the cloud.
4. Continuously improve the model by incorporating user feedback and new data.

## :hammer_and_wrench: Solution

### Core Features

- **Image Upload**: Users can upload a photo of their skin lesion.
- **AI Diagnosis**: The deep learning model analyzes the image and classifies it as malignant or benign.
- **Confidence Score**: The model provides a probability score for its prediction.
- **User Feedback Mechanism**: Users can report incorrect predictions, improving the model over time.

## :bar_chart: Data & Feasibility

### Data

We are using the **HAM10000** dataset from Kaggle: [HAM10000 Dataset](https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000)

### Team Expertise

- All team members have a solid understanding of deep learning concepts.
- Experience with CNN architectures and computer vision tasks.

### Infrastructure

- **Cloud Deployment**: The model will be hosted on **Google Cloud** to ensure accessibility and scalability.
- **Backend**: 
- **Frontend**: 

<!-- ## :triangular_ruler: Modeling

We are implementing a **CNN-based deep learning model** for image classification.
- Model trained using TensorFlow/Keras.
- Augmentation techniques to improve generalization.
- Regular evaluation to prevent overfitting. -->

## :chart_with_upwards_trend: Metrics

To assess our model's performance, we will evaluate:
- **Accuracy**: Percentage of correctly classified lesions.
- **Precision & Recall**: To balance false positives and false negatives.
- **ROC Curve & AUC Score**: To measure how well the model distinguishes between malignant and benign cases.

## :thinking: Inference

Inference will be performed in real-time using the deployed model on **Google Cloud**. Users will receive predictions within seconds of uploading an image.

## :mag_right: Evaluation & Continuous Learning

- **User Reports**: Collect user feedback on incorrect predictions.
- **Continuous Learning**: Periodically update the model with new labeled data to improve performance.

## :bricks: Building Blocks

<!-- 
| Not started | ❌    |
| In Progress | ⏳  |
| Done | ✅  |
 -->

| ID   | Week  | Task Description                                      | Status | Location | Required/Optional |
|------|------|------------------------------------------------------|--------|----------|-------------------|
| 1.1  | W01  | Form a team. | ✅ | [Our Team](#stethoscope-our-team) | Required |
| 1.2  | W02  | Select use case. | ✅ | [USECASE.md](USECASE.md) | Required |
| 1.3  | W02  | Define use case.  | ✅ | [USECASE.md](USECASE.md) | Required |
| 1.4  | W02  | Pick a creative project name. | ✅ | DeepSkin | Required |
| 1.5  | W02  | Set up a communication channel. | ✅ | Discord | Required |
| 1.6  | W02  | Create a GitHub repository for code versioning. | ✅ | [DeepSkin](https://github.com/JulienHansen/DeepSkin) | Required |
| 1.7  | W02  | Submit the project card with basic details for feedback. | ✅ | - | Required |
| 2.1  | W03  | Perform Exploratory Data Analysis (EDA). | ✅ | [Here](exploratory_data_analisi.ipynb) | Required |
| 2.2  | W03  | Set up Cloud environment (create project, grant access, set up billing). | ✅ | - | Required |
| 2.3  | W04  | Train your ML model. | ⏳ | [Training](model/train.py) | Required |
| 2.4  | W04  | Evaluate your ML model. | ⏳ | [Prediction](model/predict.py) | Required |
| 2.5  | W03-W04 | Document data analysis and model performance. | ❌ | - | Required |
| 3.1  | W05  | Build an API to serve your ML model. Run it locally. | ❌ | - | Required |
| 3.2  | W05  | Package the API in a Docker container. Run it locally. | ❌ | - | Required |
| 3.3  | W06  | Deploy the API in the Cloud, allowing remote predictions. | ❌ | - | Required |
| 4.1  | W08  | Build an automated pipeline for training & deployment (e.g., Kubeflow, Sagemaker, GCP Vertex). | ❌ | - | Optional |
| 5.1  | W09  | Run model training as a Cloud job (e.g., on a VM or managed service). | ❌ | - | Optional |
| 5.2  | W10  | Build and deploy a simple UI/dashboard to showcase results. | ❌ | - | Optional |
| 6.1  | W10  | Build a CI/CD pipeline (e.g., GitHub Actions) with at least one automated step. | ❌ | - | Required |
| 6.2  | W10  | CI/CD step: Auto-deploy model serving components. | ❌ | - | Optional |
| 6.3  | W10  | CI/CD step: Run Pylint for code quality checks. | ❌ | - | Optional |
| 6.4  | W10  | CI/CD step: Run Pytest for unit tests. | ❌ | - | Optional |
