import torch
import torch.nn as nn
import torchvision.models as models

class MultiModalLesionClassifier(nn.Module):
    def __init__(self, num_meta_features, num_classes):
        super(MultiModalLesionClassifier, self).__init__()
        
        # Image branch using a pretrained CNN (e.g., ResNet18)
        self.cnn = models.resnet18(pretrained=True)
        num_ftrs = self.cnn.fc.in_features
        self.cnn.fc = nn.Identity()  # Remove final classification layer
        
        # Metadata branch: a simple MLP
        self.meta_net = nn.Sequential(
            nn.Linear(num_meta_features, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU()
        )
        
        # Fusion and final classification
        self.classifier = nn.Sequential(
            nn.Linear(num_ftrs + 16, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes)
        )
        
    def forward(self, image, metadata):
        # Process image through CNN
        img_features = self.cnn(image)  # Shape: [batch, num_ftrs]
        
        # Process metadata through MLP
        meta_features = self.meta_net(metadata)  # Shape: [batch, 16]
        
        # Concatenate image and metadata features
        combined = torch.cat((img_features, meta_features), dim=1)
        
        # Final classification
        out = self.classifier(combined)
        return out

