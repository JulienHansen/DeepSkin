import os
import time
import gcsfs  
import torch
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm
from models.model import MultiModalLesionClassifier 
from models.data_loader import get_dataloader, HAM10000ImageDataset
from torchvision import transforms
from models.args_train import get_args_parser
from models.utils import plot_losses, download_from_gcs, upload_trained_model, save_final_model


def train(model, train_loader, test_loader, optimizer, criterion, epochs, device, save_freq, save_path):
    """
    Train the multi-modal lesion classification model.
    """
    avg_train_losses_history = []
    avg_test_losses_history = []

    for epoch in tqdm(range(epochs), desc="Training"):
        epoch_start = time.time()
        model.train()
        train_losses, train_accs = [], []

        # Training loop
        for images, metadata, labels in train_loader:
            images, metadata, labels = images.to(device), metadata.to(device), labels.to(device)
            outputs = model(images, metadata)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            train_losses.append(loss.item())
            train_accs.append((outputs.argmax(dim=1) == labels).float().mean().item())

        # Evaluation loop
        model.eval()
        test_losses, test_accs = [], []
        with torch.no_grad():
            for images, metadata, labels in test_loader:
                images, metadata, labels = images.to(device), metadata.to(device), labels.to(device)
                outputs = model(images, metadata)
                loss = criterion(outputs, labels)
                test_losses.append(loss.item())
                test_accs.append((outputs.argmax(dim=1) == labels).float().mean().item())

        avg_train_loss = np.mean(train_losses)
        avg_train_acc = np.mean(train_accs)
        avg_test_loss = np.mean(test_losses)
        avg_test_acc = np.mean(test_accs)
        epoch_time = time.time() - epoch_start

        print(f"Epoch [{epoch+1}/{epochs}] "
              f"Train Loss: {avg_train_loss:.4f}, Train Acc: {avg_train_acc:.4f} | "
              f"Test Loss: {avg_test_loss:.4f}, Test Acc: {avg_test_acc:.4f} | "
              f"Time: {epoch_time:.2f}s")

        # Save checkpoint
        if (epoch + 1) % save_freq == 0:
            checkpoint_path = os.path.join(save_path, f"model_epoch_{epoch+1}.pt")
            torch.save({
                'epoch': epoch + 1,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'train_loss': avg_train_loss,
                'test_loss': avg_test_loss,
                'train_acc': avg_train_acc,
                'test_acc': avg_test_acc,
            }, checkpoint_path)
            print(f"Saved checkpoint to {checkpoint_path}")

        avg_train_losses_history.append(avg_train_loss)
        avg_test_losses_history.append(avg_test_loss)

    # Optionally, you could plot the losses here:
    # plot_losses(avg_train_losses_history, avg_test_losses_history)

if __name__ == '__main__':
    # Parse arguments.
    parser = get_args_parser()
    args = parser.parse_args()

    # Download dataset from GCS if the local data path doesn't exist or is empty.
    if not os.path.exists(args.data_path) or not os.listdir(args.data_path):
        print("Dataset not found locally, downloading from Google Cloud Storage...")
        CSV_FILE, IMAGES_PATH_1, IMAGES_PATH_2 = download_from_gcs(args.data_path)
    else:
        CSV_FILE = os.path.join(args.data_path, 'HAM10000_metadata.csv')
        IMAGES_PATH_1 = os.path.join(args.data_path, 'HAM10000_images_part_1')
        IMAGES_PATH_2 = os.path.join(args.data_path, 'HAM10000_images_part_2')
    
    device = torch.device(args.device if torch.cuda.is_available() else 'cpu')
    num_meta_features = 3  # 'age', 'sex', and 'localization'
    num_classes = 7        

    transform_pipeline = transforms.Compose([
        transforms.Resize((args.img_size, args.img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    
    print("OK1")
    dataset = HAM10000ImageDataset(CSV_FILE, IMAGES_PATH_1, IMAGES_PATH_2,
                                   transform=transform_pipeline, max_samples=args.max_samples)
    print("OK2")

    train_loader, test_loader = get_dataloader(dataset, batch_size=args.batch_size, train_split=args.train_prop)

    model = MultiModalLesionClassifier(num_meta_features, num_classes).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    criterion = torch.nn.CrossEntropyLoss()
    
    SAVE_PATH = args.save_path
    os.makedirs(SAVE_PATH, exist_ok=True)
    
    # Start training
    train(model, train_loader, test_loader, optimizer, criterion, 
          epochs=args.epochs, device=device, save_freq=args.save_freq, save_path=SAVE_PATH)
    
    # Save the final model locally as "final_model.pt"
    final_model_local_path = save_final_model(model, SAVE_PATH)
    
    # If --on_cloud flag is provided, upload the final model to the cloud.
    if args.on_cloud:
        if not args.cloud_save_path.startswith("gs://"):
            print("Error: --cloud_save_path must be a valid GCS path (e.g. gs://bucket/path).")
            exit(1)
        upload_trained_model(final_model_local_path, args.cloud_save_path)
