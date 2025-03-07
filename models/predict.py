"""
This module provides functions for loading a pre-trained model and making predictions on images.

Functions:
- load_model(model_size, device=None): Load a pre-trained model of the specified size.
- predict(model, image, metadata): Make predictions using both image and metadata.

"""

import base64
import io
import torch
from PIL import Image, ImageFile
from torchvision import transforms
from .model import create_multimodal 
import pandas as pd

# Mapping from index to class names for HAM10000
INDEX_TO_CLASS = {
    0: 'actinic keratoses', 1: 'basal cell carcinoma', 2: 'benign keratosis-like lesions',
    3: 'dermatofibroma', 4: 'melanoma', 5: 'melanocytic nevi', 6: 'vascular lesions'
}

# Pretrained model paths
MODEL_TYPE_TO_PATH = {
    "small": "checkpoints/model_epoch_20.pt",
    "base": "models/checkpoints/ham10000_base.pt",
    "large": "models/checkpoints/ham10000_large.pt"
}

ImageFile.LOAD_TRUNCATED_IMAGES = True 

def load_model(model_size, device=None):
    """
    Load a pre-trained model for HAM10000 classification.

    Args:
        model_size (str): Model size to load ('small', 'base', or 'large').
        device (torch.device, optional): Device to load the model onto.

    Returns:
        torch.nn.Module: Loaded pre-trained model.
    """
    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    model = create_multimodal(num_meta_features=3, num_classes=7, model_size=model_size)
    checkpoint = torch.load(MODEL_TYPE_TO_PATH[model_size], map_location=device, weights_only=False)
    model.load_state_dict(checkpoint["model_state_dict"])  # Use the model's state dict
    model.to(device)
    model.eval()
    return model


def preprocess_image(image):
    """
    Preprocess the input image for the model.

    Args:
        image (bytes or str): Image data as a byte string or base64 encoded string.

    Returns:
        torch.Tensor: Preprocessed image tensor.
    """
    if isinstance(image, (bytes, str)):
        image = base64.b64decode(image)
        image = Image.open(io.BytesIO(image)).convert('RGB')

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    image = transform(image).unsqueeze(0) 
    return image

def preprocess_metadata(age, sex, localization):
    """
    Preprocess metadata features for the model.

    Args:
        age (float): Age of the patient.
        sex (str): 'male' or 'female'.
        localization (str): Body location of lesion.

    Returns:
        torch.Tensor: Preprocessed metadata tensor.
    """
    age = age / 100.0  
    sex = 0.0 if sex.lower() == 'male' else 1.0  
    localization_code = pd.Categorical([localization]).codes[0]  
    metadata = torch.tensor([[age, sex, localization_code]], dtype=torch.float32) 
    return metadata

def predict(model, image, metadata, device=None):
    """
    Make predictions using both image and metadata.

    Args:
        model (torch.nn.Module): Pre-trained model.
        image (bytes or str): Image data (base64 encoded or raw bytes).
        metadata (tuple): Tuple of (age, sex, localization).
        device (torch.device, optional): Device for computation.

    Returns:
        dict: Predicted probabilities for each class.
    """
    if device is None:
        device = next(model.parameters()).device 

    image_tensor = preprocess_image(image).to(device)
    metadata_tensor = preprocess_metadata(*metadata).to(device)


    with torch.no_grad():
        output = model(image_tensor, metadata_tensor)
        output = torch.nn.functional.softmax(output, dim=1)  

    return {INDEX_TO_CLASS[i]: output[0][i].item() for i in range(len(output[0]))}

if __name__ == '__main__':
    model = load_model('small')

    with open("test_picture.jpg", "rb") as f:
        encoded_image = base64.b64encode(f.read())

    example_metadata = (80, "male", "scalp")  # Age, Sex, Localization

    predictions = predict(model, encoded_image, example_metadata)
    print(predictions)
