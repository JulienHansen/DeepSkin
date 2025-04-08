"""
This script is used to configure the DeepSkin project as a Python package.

It defines the required dependencies and metadata for the package, enabling easy installation
and integration with tools like Vertex AI or other cloud platforms.

Key components:
- REQUIRED_PACKAGES: A list of dependencies required to run the project.
- setup(): Configures the package metadata, dependencies, and other settings.

Usage:
    Run this script to install the package:
    python setup.py install
"""

from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = [
    "torch",
    "torchvision",
    "numpy",
    "pandas",
    "Pillow",
    "scikit-learn",
    "wandb",
    "tqdm",
    "datasets",
    "cloudml-hypertune",
    "kaggle",
    "google-cloud-secret-manager"
]

setup(
    name='deepskin_vertex',
    version='0.1',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='DeepSkin vertex integration',
)
