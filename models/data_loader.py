"""
This module contains classes and functions for loading and pre-processing DeepSkin project data.

It includes:
- A `HAM10000ImageDataset` class to manage the HAM10000 dataset.
- Functions to create DataLoaders for training and testing.
- Utilities for calculating the mean and standard deviation of image channels.
- A function to denormalise images for visualisation.

Usage:
    Import this module to load and pre-process data, or run it directly to test functionality.
"""

import os
import pandas as pd
from torchvision import transforms
from torch.utils.data import random_split, Dataset, DataLoader
from PIL import Image
import torch
import matplotlib.pyplot as plt
import numpy as np


class HAM10000ImageDataset(Dataset):
    """
    Custom dataset for the HAM10000 dataset.

    This dataset manages images and associated metadata (age, sex, location) 
    for skin disease classification tasks.

    Args:
        csv_file (str): Path to the CSV file containing the metadata.
        images_path_1 (str): Path to the first folder containing the images.
        images_path_2 (str): Path to the second folder containing the images.
        transform (callable, optional): Transforms to be applied to the images (default: ToTensor).
        max_samples (int, optional): Maximum number of samples to load (default: None, loads all).

    Attributes:
        data (pd.DataFrame): DataFrame containing image metadata and paths.
        class_names (list): List of class names.
        class_to_idx (dict): Dictionary mapping class names to their indices.
        len_data (int): Total number of samples in the dataset.
    """
    def __init__(self, csv_file, images_path_1, images_path_2, transform=None, max_samples=None):
        self.transform = transform if transform is not None else transforms.ToTensor()

        # Load metadata CSV
        self.data = pd.read_csv(csv_file)

        dx_mapping = {
            'akiec': 'actinic keratoses',
            'bcc': 'basal cell carcinoma',
            'bkl': 'benign keratosis-like lesions',
            'df': 'dermatofibroma',
            'mel': 'melanoma',
            'nv': 'melanocytic nevi',
            'vasc': 'vascular lesions'
        }
        self.data['dx'] = self.data['dx'].map(dx_mapping)

        self.data['image_path'] = self.data['image_id'].apply(
            lambda x: os.path.join(images_path_1, x + '.jpg')
            if os.path.exists(os.path.join(images_path_1, x + '.jpg'))
            else os.path.join(images_path_2, x + '.jpg')
        )

        if max_samples:
            self.data = self.data.head(max_samples)

        self.len_data = len(self.data)

        self.class_names = sorted(self.data['dx'].unique())
        self.class_to_idx = {label: i for i, label in enumerate(self.class_names)}

        # Preprocess metadata (age, sex, localization)
        self.data.loc[:, 'age'] = self.data['age'].fillna(self.data['age'].median()) / 100.0

        # Clean and process the 'sex' column.
        def map_sex(sex_value):
            sex_value = str(sex_value).lower().strip() if pd.notnull(sex_value) else ""
            if sex_value in ['male', 'm']:
                return 0.0
            if sex_value in ['female', 'f']:
                return 1.0

            # Map unknown or unexpected values to 0.5
            return 0.5

        self.data.loc[:, 'sex'] = self.data['sex'].apply(map_sex)
        self.data.loc[:, 'localization'] = self.data['localization'].fillna('unknown')
        self.data.loc[:, 'localization'] = self.data['localization'].astype('category').cat.codes
        #print(self.data[['age', 'sex', 'localization']].isnull().sum())

    def __len__(self):
        return self.len_data

    def get_nb_classes(self):
        """
        Get the number of unique classes in the dataset.

        Returns:
            int: The number of unique classes.
        """
        return len(self.class_names)

    def get_class_to_idx(self):
        """
        Get the mapping of class names to their corresponding indices.

        Returns:
            dict: A dictionary where keys are class names and values are their indices.
        """
        return self.class_to_idx

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        image_path = row['image_path']

        image = Image.open(image_path).convert('RGB')
        if self.transform:
            image = self.transform(image)

        label = torch.tensor(self.class_to_idx[row['dx']], dtype=torch.long)
        # Get metadata as a tensor: [age, sex, localization]
        metadata = torch.tensor([row['age'], row['sex'], row['localization']], dtype=torch.float32)

        return image, metadata, label  # Now returns three values


def get_dataloader(input_dataset, batch_size, train_split=0.8):
    """
    Create data loaders for training and testing.

    Args:
        input_dataset (Dataset): Dataset object.
        batch_size (int): Batch size.
        train_split (float, optional): Proportion of data for training.

    Returns:
        tuple: (train_loader, test_loader)
    """
    train_size = int(train_split * len(input_dataset))
    test_size = len(input_dataset) - train_size
    train_dataset, test_dataset = random_split(input_dataset, [train_size, test_size])

    train_data_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_data_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_data_loader, test_data_loader

def get_mean_std(input_dataset, batch_size):
    """
    Compute the per-channel mean and standard deviation for the dataset.

    Args:
        dataset (Dataset): The dataset object.
        batch_size (int): Batch size for the DataLoader.

    Returns:
        tuple: (mean, std) as torch.Tensors.
    """
    dataloader = DataLoader(input_dataset, batch_size=batch_size, shuffle=False)
    channel_mean = torch.zeros(3)
    channel_std = torch.zeros(3)
    nb_samples = 0

    for images, _ in dataloader:
        batch_samples = images.size(0)
        images = images.view(batch_samples, images.size(1), -1)
        channel_mean += images.mean(2).sum(0)
        channel_std += images.std(2).sum(0)
        nb_samples += batch_samples
    channel_mean /= nb_samples
    channel_std /= nb_samples
    return channel_mean, channel_std

def unnormalize(img, input_mean, input_std):
    """
    Unnormalize a tensor image and convert it to a NumPy array for visualization.
    
    Args:
        img (torch.Tensor): Normalized image tensor.
        mean (list or np.array): Mean used for normalization.
        std (list or np.array): Standard deviation used for normalization.
        
    Returns:
        np.array: Unnormalized image as a NumPy array.
    """
    img = img.cpu().numpy().transpose(1, 2, 0)
    img = input_std * img + input_mean
    img = np.clip(img, 0, 1)
    return img

if __name__ == '__main__':
    CSV_FILE = '../archive/HAM10000_metadata.csv'
    IMAGES_PATH_1 = '../archive/HAM10000_images_part_1/'
    IMAGES_PATH_2 = '../archive/HAM10000_images_part_2/'
    BATCH_SIZE = 32
    MAX_SAMPLES = 1000

    # Define the image transformation pipeline.
    transform_pipeline = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    # Create the dataset.
    dataset = HAM10000ImageDataset(
        csv_file=CSV_FILE,
        images_path_1=IMAGES_PATH_1,
        images_path_2=IMAGES_PATH_2,
        transform=transform_pipeline,
        max_samples=MAX_SAMPLES
    )

    # Create data loaders.
    train_loader, test_loader = get_dataloader(dataset, BATCH_SIZE)

    print("Train samples:", len(train_loader) * BATCH_SIZE)
    print("Test samples:", len(test_loader) * BATCH_SIZE)

    mean, std = get_mean_std(dataset, batch_size=256)
    print('Mean:', mean)
    print('Std:', std)

    img_mean = np.array([0.485, 0.456, 0.406])
    img_std = np.array([0.229, 0.224, 0.225])

    train_images, train_labels = next(iter(train_loader))
    test_images, test_labels = next(iter(test_loader))

    # Select the first image from each batch.
    train_img = train_images[0]
    test_img = test_images[0]

    # Unnormalize the images.
    train_img_np = unnormalize(train_img, img_mean, img_std)
    test_img_np = unnormalize(test_img, img_mean, img_std)

    # Plot the images.
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(train_img_np)
    plt.title("Train Set Sample")
    plt.axis("off")
    plt.subplot(1, 2, 2)
    plt.imshow(test_img_np)
    plt.title("Test Set Sample")
    plt.axis("off")
    plt.show()
