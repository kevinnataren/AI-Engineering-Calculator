#!/bin/bash
set -e

echo "Installing Raspberry Pi system packages..."
sudo apt update
sudo apt install -y python3-venv python3-tk python3-sympy rpicam-apps

echo "Creating Python virtual environment..."
python3 -m venv --system-site-packages venv

echo "Installing calculator Python packages..."
venv/bin/pip install -r requirements.txt

echo "AI Calculator setup complete."
