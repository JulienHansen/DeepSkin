import matplotlib.pyplot as plt

import os
import gcsfs
import torch


def upload_trained_model(final_model_local_path, cloud_save_path):
    """
    Empties the cloud folder of any existing "final_model.pt" file and uploads the final model.
    """
    fs = gcsfs.GCSFileSystem()

    # List and remove any existing "final_model.pt" in the cloud_save_path
    try:
        files = fs.ls(cloud_save_path)
        for file in files:
            if os.path.basename(file) == "final_model.pt":
                fs.rm(file)
                print(f"Deleted existing file {file} from cloud storage.")
    except Exception as e:
        print(f"Error listing files in {cloud_save_path} or no files to delete: {e}")

    # Define destination and upload the final model
    destination = os.path.join(cloud_save_path, "final_model.pt")
    fs.put(final_model_local_path, destination)
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
    plt.plot(range(1, len(train_losses) + 1), train_losses, label='Train Loss', marker='o', color='royalblue', markersize=8, linewidth=2, linestyle='-', alpha=0.8)
    plt.plot(range(1, len(test_losses) + 1), test_losses, label='Test Loss', marker='x', color='tomato', markersize=8, linewidth=2, linestyle='--', alpha=0.8)

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
    fs = gcsfs.GCSFileSystem()

    # GCS Paths
    GCS_CSV_PATH = 'gs://deepskin_dataset/archive/HAM10000_metadata.csv'
    GCS_IMAGES_PATH_1 = 'gs://deepskin_dataset/archive/HAM10000_images_part_1/'
    GCS_IMAGES_PATH_2 = 'gs://deepskin_dataset/archive/HAM10000_images_part_2/'

    # Local Paths based on the given local_data_path
    LOCAL_CSV_PATH = os.path.join(local_data_path, "HAM10000_metadata.csv")
    LOCAL_IMAGES_PATH_1 = os.path.join(local_data_path, "HAM10000_images_part_1")
    LOCAL_IMAGES_PATH_2 = os.path.join(local_data_path, "HAM10000_images_part_2")

    # Create the base data directory if it doesn't exist
    os.makedirs(local_data_path, exist_ok=True)

    # Download CSV if it doesn't exist
    if not os.path.exists(LOCAL_CSV_PATH):
        print("Downloading metadata CSV...")
        fs.get(GCS_CSV_PATH, LOCAL_CSV_PATH)

    # Download images from each GCS path if they are not already downloaded
    for gcs_path, local_path in [(GCS_IMAGES_PATH_1, LOCAL_IMAGES_PATH_1), (GCS_IMAGES_PATH_2, LOCAL_IMAGES_PATH_2)]:
        # Check if the folder exists and is non-empty
        if not os.path.exists(local_path) or len(os.listdir(local_path)) == 0:
            print(f"Downloading images from {gcs_path} to {local_path}...")
            os.makedirs(local_path, exist_ok=True)
            files = fs.ls(gcs_path)
            # Filter only image files (adjust extensions as necessary)
            image_files = [file for file in files if file.lower().endswith(('.jpg', '.jpeg', '.png'))]
            for file in image_files:
                local_file = os.path.join(local_path, os.path.basename(file))
                fs.get(file, local_file)
                print(f"Downloaded {file} to {local_file}")

    print("Dataset download complete!")
    return LOCAL_CSV_PATH, LOCAL_IMAGES_PATH_1, LOCAL_IMAGES_PATH_2

