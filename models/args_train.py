import argparse

def get_args_parser():
    """
    Get the argument parser.

    Returns:
        ArgumentParser: An ArgumentParser object configured with various options.
    """
    parser = argparse.ArgumentParser("DEEPSKIN", add_help=False)

    # Checkpoints
    parser.add_argument("--save_path", type=str, default="./weights", help="Path to save the checkpoints")
    parser.add_argument("--save_freq", type=int, default=5, help="Save frequency")

    # Dataset
    parser.add_argument("--data_path", type=str, default="./data", help="Path to the data")
    parser.add_argument("--img_size", type=int, default=224, help="Size of the images")

    # Training parameters
    parser.add_argument("--epochs", type=int, default=10, help="Number of epochs")
    parser.add_argument("--optimizer", type=str, default="AdamW", help="Optimizer")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")
    parser.add_argument("--train_prop", type=float, default=0.80, help="Proportion of the data used for training")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size")
    parser.add_argument("--max_samples", type=int, default=100, help="Maximum number of samples to use")
    parser.add_argument("--seed", type=int, default=42, help="Seed for the random number generator")
    parser.add_argument("--device", type=str, default="cuda", help="Device to use to train the model")
    parser.add_argument("--load_all_in_ram", action="store_true", help="Load all the data in RAM")
        
    # Cloud upload options
    parser.add_argument("--on_cloud", action="store_true", help="Upload the trained model to the cloud (empties bucket before uploading).")
    parser.add_argument("--cloud_save_path", type=str, default="gs://trained_deepskin_model/", help="GCS path to upload the final model (e.g. gs://bucket/path).")

    return parser

