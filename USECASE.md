# Machine Learning Canvas


## Background

Skin cancer is one of the most common forms of cancer, early detection is crucial for effective treatment. Many people around the world lack easy access to proper medical attention.
Our project aims at enabeling our users to determine wheter their mark/lesions is malicious or not and if medical attention is necessary.

## Value Proposition

We propose an application for automatically identifying nature and potential risk assessment of user's lesions. Users do not need to have any medical knowledge. This reduces unnecessary visits for benign cases while ensuring that high-risk cases receive urgent medical attention.


## Objectives

1. Provide the user with a interactive and easy to use interface to use our model.
2. Classify the nature of the lesion, and give a probability score on the prediction.

## Solution 

- `core features`: Users upload images and the model predict the specific nature of the problem



## Feasibility

- `data`: We use this [dataset](https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000)
- `team`: We are all familiar with Deep learning notion 
- `infrastructure`:
    - `cloud`: We will use Google Cloud to deploy our model


## Data

- Kaggle [dataset](https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000)

## Metrics

- Accuracy: Percentage of correctly classified lesions
- Precision & Recall: Measures to balance false positives from false negatives
- ROC curve: Evaluate model in distinguishing malignant vs benign cases.


## Evaluation

# Offline evaluation

- Data separation: Separate data into training, validation and test sets to avoid overlearning.
- Error analysis: Identify the types of images or lesions on which the model fails, such as blurred or poorly lit lesions.
- Cross-validation: Use cross-validation to test the generalizability of the model on several subsets of the data.

# Online evaluation

- User feedback: Gather feedback from users (dermatologists, patients) to fine-tune the model and its accuracy in a real-life context.
- Error management: In the event of incorrect predictions, adjust the model or alert users to take further action.
- Latency: Monitor the speed of model predictions to ensure rapid response.


## Modeling

CNN-based Deep learning model

## Inference

?

## Feedback

- User Reports: collect feedback on incorrect predictions made
- Continuous Learning: Update the model with new labeled data 

## Project

Our whole project statement is available here [Project Statement]()


