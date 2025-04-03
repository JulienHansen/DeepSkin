"""
This module defines the MultiModalLesionClassifier, a deep learning 
model for skin lesion classification.

The model combines two branches:
- An image branch using a pretrained ResNet18 for processing image data.
- A metadata branch using a simple MLP for processing patient metadata 
  (e.g., age, sex, localization).

The features from both branches are fused and passed through a fully connected 
classifier to predict the lesion class.

Usage:
    Import this module and instantiate the `MultiModalLesionClassifier` 
    with the required number of metadata features
    and output classes. Use the `forward` method to perform inference.

Example:
    model = MultiModalLesionClassifier(num_meta_features=3, num_classes=7)
    output = model(image_tensor, metadata_tensor)
"""

import torch
from torch import nn
from torchvision import models
from torchvision.models import ResNet18_Weights

class MultiModalLesionClassifier(nn.Module):
    """
    Multi-Modal Lesion Classifier

    This model combines a pretrained CNN (ResNet18) for image processing with a simple
    MLP for metadata processing. The features from both branches are fused and passed
    through a classifier.

    Args:
        num_meta_features (int): Number of features in the metadata.
        num_classes (int): Number of output classes.
    """
    def __init__(self, num_meta_features, num_classes):
        super(MultiModalLesionClassifier, self).__init__()

        # Configuration for the base model
        meta_hidden = 32
        classifier_layers = [64, 128, 256]

        # Image branch: Pretrained ResNet18
        self.cnn = models.resnet18(weights=None)
        num_ftrs = self.cnn.fc.in_features
        self.cnn.fc = nn.Identity()  # Remove the original fully connected layer

        # Metadata branch: A simple MLP with two layers
        self.meta_net = nn.Sequential(
            nn.Linear(num_meta_features, meta_hidden),
            nn.ReLU(),
            nn.Linear(meta_hidden, meta_hidden),
            nn.ReLU()
        )

        # Fusion and final classification
        fusion_input_size = num_ftrs + meta_hidden
        layers = []
        for out_features in classifier_layers:
            layers.append(nn.Linear(fusion_input_size, out_features))
            layers.append(nn.ReLU())
            fusion_input_size = out_features
        layers.append(nn.Linear(fusion_input_size, num_classes))
        self.classifier = nn.Sequential(*layers)

    def forward(self, image, metadata):
        """
        Perform a forward pass through the MultiModalLesionClassifier.

        This method processes the input image and metadata through their respective branches,
        combines the extracted features, and passes them through the classifier to produce
        the final output.

        Args:
            image (torch.Tensor): A tensor representing the input image batch, with shape 
            (batch_size, channels, height, width).
            metadata (torch.Tensor): A tensor representing the metadata batch, with shape 
            (batch_size, num_meta_features).

        Returns:
            torch.Tensor: The model's output logits, with shape (batch_size, num_classes).
        """
        # Process image branch
        img_features = self.cnn(image)
        # Process metadata branch
        meta_features = self.meta_net(metadata)
        # Concatenate features and classify
        combined = torch.cat((img_features, meta_features), dim=1)
        out = self.classifier(combined)
        return out

    @property
    def n_params(self):
        """Return the number of trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


if __name__ == '__main__':
    NUM_META_FEATURES = 3
    NUM_CLASSES = 7

    base_model = MultiModalLesionClassifier(NUM_META_FEATURES, NUM_CLASSES)
    print('Base model parameters:', base_model.n_params)
