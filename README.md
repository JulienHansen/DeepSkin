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

Here is a table summarizing all the features implemented in this project
| Feature | Status |
|---------|--------|
|         |        |
