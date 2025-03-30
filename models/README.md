🧠 Models

This document provides an overview of the model architecture we utilized. The folder follows a classical deep learning project structure.

⚙️ Architecture

Our model employs a hybrid architecture to effectively leverage the information available in the HAM10000 dataset. We utilize both image features extracted through a pre-trained ResNet-18 model and accompanying meta-data. The meta-data is processed through a classical Multi-Layer Perceptron (MLP) and subsequently concatenated with the output of the ResNet model. The combined output is then passed through a final MLP to produce the prediction.

📈 Model Performance Metrics

The performance of each model variant is evaluated using two primary metrics:

Global Accuracy: Reflects the overall accuracy of the model across all seven classes included in the training dataset.

Binary Accuracy (Not Implemented): Placeholder for binary accuracy metric implementation.

📊 Performance Comparison

The accuracy of our model, as well as the training and testing loss, can be found in the plot.ipynb Jupyter notebook.

⚙️ Parser and Hyperparameter Configuration

To simplify model usage and facilitate future integration with Vertex AI, we implemented a classical parser to manage all hyperparameter values. This allows for easy modification and parameter passing within our model.
