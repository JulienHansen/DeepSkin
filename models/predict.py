"""
This module provides functions for loading a pre-trained base model and making predictions on images.

Functions:
- load_model(checkpoint_path, device=None): Load a pre-trained base model from the specified checkpoint path.
- predict(model, image, metadata): Make predictions using both image and metadata.
"""

import base64
import io
import torch
from PIL import Image, ImageFile
from torchvision import transforms
from .model import MultiModalLesionClassifier  # Ensure this import matches your project structure
import pandas as pd

# Mapping from index to class names for HAM10000
INDEX_TO_CLASS = {
    0: 'actinic keratoses', 1: 'basal cell carcinoma', 2: 'benign keratosis-like lesions',
    3: 'dermatofibroma', 4: 'melanoma', 5: 'melanocytic nevi', 6: 'vascular lesions'
}

ImageFile.LOAD_TRUNCATED_IMAGES = True

def load_model(checkpoint_path, device=None):
    """
    Load a pre-trained base model for HAM10000 classification from a specified checkpoint path.

    Args:
        checkpoint_path (str): Local path to the model checkpoint.
        device (torch.device, optional): Device to load the model onto.

    Returns:
        torch.nn.Module: Loaded pre-trained base model.
    """
    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Initialize the base model
    model = MultiModalLesionClassifier(num_meta_features=3, num_classes=7)
    model.to(device)

    # Load checkpoint
    checkpoint = torch.load(checkpoint_path, map_location=device, weights_only=False)

    # Filter out mismatched keys
    model_dict = model.state_dict()
    filtered_dict = {k: v for k, v in checkpoint['model_state_dict'].items() if k in model_dict and v.size() == model_dict[k].size()}

    # Update the existing model's state_dict
    model_dict.update(filtered_dict)

    # Load the new state_dict
    model.load_state_dict(model_dict)

    model.eval()
    return model

def preprocess_image(image):
    """
    Preprocess the input image for the model.

    Args:
        image (bytes or str): Image data as a raw byte string, file path, or base64 encoded string.

    Returns:
        torch.Tensor: Preprocessed image tensor.
    """
    # If the input is a string, check if it's a valid file path.
    if isinstance(image, str):
        if os.path.exists(image):
            # It's a file path; open it directly.
            image = Image.open(image).convert('RGB')
        else:
            # Otherwise, assume it's a base64 encoded string.
            try:
                decoded = base64.b64decode(image)
                image = Image.open(io.BytesIO(decoded)).convert('RGB')
            except Exception as e:
                raise ValueError("The string provided is neither a valid file path nor a proper base64 encoded image.") from e
    elif isinstance(image, bytes):
        # Try opening the bytes directly.
        try:
            image = Image.open(io.BytesIO(image)).convert('RGB')
        except Exception:
            # If that fails, assume the bytes are actually base64-encoded.
            try:
                decoded = base64.b64decode(image)
                image = Image.open(io.BytesIO(decoded)).convert('RGB')
            except Exception as e:
                raise ValueError("The bytes provided are neither a valid raw image nor a proper base64 encoded image.") from e
    else:
        raise TypeError("Unsupported type for image. Must be bytes or str.")

    # Define the transform for the image.
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
        age (float or str): Age of the patient.
        sex (str): 'male' or 'female'.
        localization (str): Body location of lesion.

    Returns:
        torch.Tensor: Preprocessed metadata tensor.
    """
    # Ensure age is a float
    age = float(age)  # Convert to float if it isn't already
    
    age = age / 100.0  # Normalize age
    sex = 0.0 if sex.lower() == 'male' else 1.0  # Encode sex
    localization_code = pd.Categorical([localization]).codes[0]  # Encode localization
    
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
    checkpoint_path = 'models/checkpoints/final_model.pt'  # Path to your base model checkpoint
    model = load_model(checkpoint_path)

    with open("models/ISIC_0024306.jpg", "rb") as f:
        encoded_image = base64.b64encode(f.read())

    example_metadata = (80, "male", "scalp")  # Age, Sex, Localization

    predictions = predict(model, encoded_image, example_metadata)
    print(predictions)
