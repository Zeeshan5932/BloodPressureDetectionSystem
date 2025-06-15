#!/bin/bash

# Install specific version of OpenCV
pip uninstall -y opencv-python opencv-python-headless
pip install opencv-python-headless==4.6.0.66

# Make sure all system dependencies are available
apt-get update
apt-get install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev

echo "Setup completed successfully."
