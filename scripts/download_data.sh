#!/bin/bash

echo "Downloading Audio Speech Sentiment dataset from Kaggle..."

# Create data directory
mkdir -p data

# Download dataset
curl -L -o ~/Downloads/audio-speech-sentiment.zip \
  https://www.kaggle.com/api/v1/datasets/download/imsparsh/audio-speech-sentiment

# Extract to data directory
if [ -f ~/Downloads/audio-speech-sentiment.zip ]; then
    echo "Extracting dataset..."
    unzip -o ~/Downloads/audio-speech-sentiment.zip -d data/
    rm ~/Downloads/audio-speech-sentiment.zip
    echo "Dataset extracted to data/"
else
    echo "Download failed. Please check your Kaggle API access."
    echo "Alternative: Download manually from https://www.kaggle.com/datasets/imsparsh/audio-speech-sentiment"
fi
