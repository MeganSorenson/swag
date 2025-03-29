#!/bin/bash

# Load environment variables from .env file
export $(grep -v '^#' .env | xargs)

# Check if ROBOFLOW_API_KEY is set
if [ -z "$ROBOFLOW_API_KEY" ]; then
    echo "Error: ROBOFLOW_API_KEY is not set in .env file"
    exit 1
fi

# Run the Flask server
python server.py 