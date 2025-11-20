#!/bin/bash

APP_DIR="/var/www/my_flask_app" # This should match your deployment directory

echo "--- Starting Deployment Script ---"

# 1. Navigate to the application directory
cd $APP_DIR

# 2. Pull the latest code from Git
echo "Pulling latest code from main branch..."
git pull origin main

# 3. Reinstall dependencies (in case they changed)
# Using `pip install -r` will only install missing/updated packages, making it fast.
echo "Installing/updating dependencies..."
# Ensure you use the same Python executable path as in your systemd service
sudo /usr/bin/pip3 install -r requirements.txt

# 4. Restart the Gunicorn service
echo "Restarting the 'myapp' Gunicorn service..."
sudo systemctl restart myapp

echo "Deployment successful! Check 'sudo systemctl status myapp' for details."