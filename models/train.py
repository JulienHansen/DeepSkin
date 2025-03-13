import os
import time
from tqdm import tqdm
import numpy as np
import torch
import matplotlib.pyplot as plt
from model import MultiModalLesionClassifier  # Ensure this matches your model's import path
from data_loader import get_dataloader, HAM10000ImageDataset  # Ensure this matches your data loader's import path
from torchvision import transforms

def train(model, train_loader, test_loader, optimizer, criterion, epochs, device, save_freq, save_path):
    """
    Train the multi-modal lesion classification model.

    Args:
        model (torch.nn.Module): The model to train.
        train_loader (DataLoader): DataLoader for training data (batches of (image, metadata, label)).
        test_loader (DataLoader): DataLoader for testing data.
        optimizer (torch.optim.Optimizer): Optimizer.
        criterion (torch.nn.Module): Loss function.
        epochs (int): Number of epochs to train.
        device (torch.device): Device on which to run training.
        save_freq (int): Frequency (in epochs) to save checkpoints.
        save_path (str): Directory path to save model checkpoints.
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

        # Store losses for plotting
        avg_train_losses_history.append(avg_train_loss)
        avg_test_losses_history.append(avg_test_loss)

    # Plot the losses after training
    plot_losses(avg_train_losses_history, avg_test_losses_history)

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



if __name__ == '__main__':

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    num_meta_features = 3  # metadata  include 'age' and 'sex' and 'localization'
    num_classes = 7        

    # Dataset paths
    CSV_FILE = '../archive/HAM10000_metadata.csv'
    IMAGES_PATH_1 = '../archive/HAM10000_images_part_1/'
    IMAGES_PATH_2 = '../archive/HAM10000_images_part_2/'
    transform_pipeline = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])
    

    dataset = HAM10000ImageDataset(CSV_FILE, IMAGES_PATH_1, IMAGES_PATH_2,
                                   transform=transform_pipeline, max_samples=10000)

    train_loader, test_loader = get_dataloader(dataset, batch_size=32, train_split=0.8)

    model = MultiModalLesionClassifier(num_meta_features, num_classes).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = torch.nn.CrossEntropyLoss()
    
    EPOCHS = 10
    SAVE_FREQ = 5
    SAVE_PATH = './checkpoints'
    os.makedirs(SAVE_PATH, exist_ok=True)
    
    # Start training.
    train(model, train_loader, test_loader, optimizer, criterion, 
          epochs=EPOCHS, device=device, save_freq=SAVE_FREQ, save_path=SAVE_PATH)

