"""
This module provides utility functions for the DeepSkin project.

It includes:
- Functions for uploading and downloading files to/from Google Cloud Storage (GCS).
- A function to save the final trained model locally.
- A function to plot training and test losses over epochs.

Functions:
- upload_trained_model: Removes existing files in a GCS folder and uploads the final model.
- save_final_model: Saves the trained model locally as 'final_model.pt'.
- plot_losses: Plots the training and test losses over epochs and saves the plot as
  'losses_plot.png'.
- download_from_gcs: Downloads the dataset (images and metadata) from GCS to a local directory.

Usage:
    Import this module to use the utility functions in your training or evaluation scripts.
"""

import os
import matplotlib.pyplot as plt
import gcsfs
import torch


def upload_trained_model(final_model_local_path, cloud_save_path):
    """
    Empties the cloud folder of any existing "final_model.pt" file and uploads the final model.
    """
    gcs_file_system = gcsfs.GCSFileSystem()

    # List and remove any existing "final_model.pt" in the cloud_save_path
    try:
        files = gcs_file_system.ls(cloud_save_path)
        for file in files:
            if os.path.basename(file) == "final_model.pt":
                gcs_file_system.rm(file)
                print(f"Deleted existing file {file} from cloud storage.")
    except (FileNotFoundError, PermissionError) as error:
        print(f"Error listing files in {cloud_save_path} or no files to delete: {error}")

    # Define destination and upload the final model
    destination = os.path.join(cloud_save_path, "final_model.pt")
    gcs_file_system.put(final_model_local_path, destination)
    print(f"Uploaded final model to {destination}")


def save_final_model(model, save_path):
    """
    Saves the final trained model locally as 'final_model.pt'.
    """
    os.makedirs(save_path, exist_ok=True)
    final_model_local_path = os.path.join(save_path, 'final_model.pt')
    torch.save({'model_state_dict': model.state_dict()}, final_model_local_path)
    print(f"Final model saved locally to {final_model_local_path}")
    return final_model_local_path



def plot_losses(train_losses, test_losses):
    """
    Plots the training and test losses over epochs.

    Parameters:
    - train_losses: List of training losses.
    - test_losses: List of test losses.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(train_losses) + 1), train_losses, label='Train Loss', marker='o',
             color='royalblue', markersize=8, linewidth=2, linestyle='-', alpha=0.8)
    plt.plot(range(1, len(test_losses) + 1), test_losses, label='Test Loss', marker='x',
             color='tomato', markersize=8, linewidth=2, linestyle='--', alpha=0.8)

    plt.xlabel('Epochs', fontsize=14, fontweight='bold', color='darkblue')
    plt.ylabel('Loss', fontsize=14, fontweight='bold', color='darkblue')
    plt.title('Training and Test Losses over Epochs', fontsize=16, fontweight='bold', color='black')

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=12, loc='best', frameon=True, framealpha=0.8, facecolor='lightgray')

    plt.savefig('losses_plot.png', dpi=300)
    plt.tight_layout()
    plt.show()


def download_from_gcs(local_data_path):
    """
    Downloads dataset from Google Cloud Storage (GCS) and stores it locally.
    Uses the specified local_data_path to download all files.
    """
    gcs_file_system = gcsfs.GCSFileSystem()

    # GCS Paths
    gcs_csv_path = 'gs://deepskin_dataset/archive/HAM10000_metadata.csv'
    gcs_images_path_1 = 'gs://deepskin_dataset/archive/HAM10000_images_part_1/'
    gcs_images_path_2 = 'gs://deepskin_dataset/archive/HAM10000_images_part_2/'

    # Local Paths based on the given local_data_path
    local_csv_path = os.path.join(local_data_path, "HAM10000_metadata.csv")
    local_images_path_1 = os.path.join(local_data_path, "HAM10000_images_part_1")
    local_images_path_2 = os.path.join(local_data_path, "HAM10000_images_part_2")

    # Create the base data directory if it doesn't exist
    os.makedirs(local_data_path, exist_ok=True)

    # Download CSV if it doesn't exist
    if not os.path.exists(local_csv_path):
        print("Downloading metadata CSV...")
        gcs_file_system.get(gcs_csv_path, local_csv_path)

    # Download images from each GCS path if they are not already downloaded
    for gcs_path, local_path in [(gcs_images_path_1, local_images_path_1),
                                 (gcs_images_path_2, local_images_path_2)]:
        # Check if the folder exists and is non-empty
        if not os.path.exists(local_path) or len(os.listdir(local_path)) == 0:
            print(f"Downloading images from {gcs_path} to {local_path}...")
            os.makedirs(local_path, exist_ok=True)
            files = gcs_file_system.ls(gcs_path)
            # Filter only image files (adjust extensions as necessary)
            image_files = [file for file in files if file.lower().endswith(
                                                ('.jpg', '.jpeg', '.png'))]
            for file in image_files:
                local_file = os.path.join(local_path, os.path.basename(file))
                gcs_file_system.get(file, local_file)
                print(f"Downloaded {file} to {local_file}")

    print("Dataset download complete!")
    return local_csv_path, local_images_path_1, local_images_path_2
