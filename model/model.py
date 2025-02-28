import torch
import torch.nn as nn
import torchvision.models as models

class MultiModalLesionClassifier(nn.Module):
    """
    Multi-Modal Lesion Classifier

    This model combines a pretrained CNN (ResNet18) for image processing with a simple
    MLP for metadata processing. The features from both branches are fused and passed
    through a classifier. The architecture supports multiple model sizes (small, base, large),
    which control the size of the metadata branch and the classifier layers.

    Args:
        num_meta_features (int): Number of features in the metadata.
        num_classes (int): Number of output classes.
        model_size (str): Model size variant ('small', 'base', or 'large').
    """
    def __init__(self, num_meta_features, num_classes, model_size='base'):
        super(MultiModalLesionClassifier, self).__init__()
        
        # Define configurations for different model sizes.
        model_sizes = {
            'small': {'meta_hidden': 16, 'classifier_layers': [64, 128]},
            'base':  {'meta_hidden': 32, 'classifier_layers': [64, 128, 256]},
            'large': {'meta_hidden': 64, 'classifier_layers': [64, 128, 256, 512]}
        }
        if model_size not in model_sizes:
            raise ValueError("Invalid model_size. Choose from 'small', 'base', or 'large'.")
        config = model_sizes[model_size]
        
        # Image branch: Pretrained ResNet18 with final FC layer removed.
        self.cnn = models.resnet18(weights=True)
        num_ftrs = self.cnn.fc.in_features
        self.cnn.fc = nn.Identity()
        
        # Metadata branch: A simple MLP with two layers.
        self.meta_net = nn.Sequential(
            nn.Linear(num_meta_features, config['meta_hidden']),
            nn.ReLU(),
            nn.Linear(config['meta_hidden'], config['meta_hidden']),
            nn.ReLU()
        )
        
        # Fusion and final classification.
        fusion_input_size = num_ftrs + config['meta_hidden']
        classifier_layers = []
        for out_features in config['classifier_layers']:
            classifier_layers.append(nn.Linear(fusion_input_size, out_features))
            classifier_layers.append(nn.ReLU())
            fusion_input_size = out_features
        classifier_layers.append(nn.Linear(fusion_input_size, num_classes))
        self.classifier = nn.Sequential(*classifier_layers)
    
    def forward(self, image, metadata):
        # Process image branch.
        img_features = self.cnn(image)  
        # Process metadata branch.
        meta_features = self.meta_net(metadata)  
        # Concatenate features and classify.
        combined = torch.cat((img_features, meta_features), dim=1)
        out = self.classifier(combined)
        return out
    
    @property
    def n_params(self):
        """Return the number of trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

# Functions to create model variants.
def multimodal_small(num_meta_features, num_classes):
    """
    Create a small Multi-Modal Lesion Classifier.
    """
    return MultiModalLesionClassifier(num_meta_features, num_classes, model_size='small')

def multimodal_base(num_meta_features, num_classes):
    """
    Create a base Multi-Modal Lesion Classifier.
    """
    return MultiModalLesionClassifier(num_meta_features, num_classes, model_size='base')

def multimodal_large(num_meta_features, num_classes):
    """
    Create a large Multi-Modal Lesion Classifier.
    """
    return MultiModalLesionClassifier(num_meta_features, num_classes, model_size='large')

def create_multimodal(num_meta_features, num_classes, model_size):
    """
    Create a Multi-Modal Lesion Classifier of a specified size.
    
    Args:
        num_meta_features (int): Number of metadata features.
        num_classes (int): Number of output classes.
        model_size (str): One of 'small', 'base', or 'large'.
    
    Returns:
        MultiModalLesionClassifier: The model instance.
    """
    if model_size == 'small':
        return multimodal_small(num_meta_features, num_classes)
    elif model_size == 'base':
        return multimodal_base(num_meta_features, num_classes)
    elif model_size == 'large':
        return multimodal_large(num_meta_features, num_classes)
    else:
        raise ValueError("Invalid model size: choose from 'small', 'base', 'large'.")

if __name__ == '__main__':
    # Example usage:
    # Assume the metadata has 2 features (for example, age and sex) and there are 7 classes.
    NUM_META_FEATURES = 3
    NUM_CLASSES = 7
    
    small_model = multimodal_small(NUM_META_FEATURES, NUM_CLASSES)
    print('Small model parameters:', small_model.n_params)
    
    base_model = multimodal_base(NUM_META_FEATURES, NUM_CLASSES)
    print('Base model parameters:', base_model.n_params)
    
    large_model = multimodal_large(NUM_META_FEATURES, NUM_CLASSES)
    print('Large model parameters:', large_model.n_params)
