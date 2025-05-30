#!/bin/bash


# Exit immediately if a command exits with a non-zero status
set -e

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the application
echo "Starting Pomodoro Timer..."
python src/main.py

# Deactivate virtual environment
deactivate