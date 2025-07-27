#!/bin/bash

echo "Setting up Audio Sentiment Analysis project..."

# Check if uv is installed, if not install it
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    pip install uv
fi

# Create virtual environment
echo "Creating virtual environment..."
uv venv venv --python 3.9

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies in virtual environment
echo "Installing dependencies..."
uv pip install -r requirements.txt

# Create directories
mkdir -p data models logs

# Download dataset
python scripts/download_data.py

echo "Setup complete!"
echo "Next steps:"
echo "  source venv/bin/activate"
echo "  python src/training/train.py"
echo "  mlflow ui --host 0.0.0.0 --port 5001 &"
echo "  uvicorn src.deployment.api:app --host 0.0.0.0 --port 8000 &"
echo "  python src/pipeline.py"
echo ""
echo "🔗 Useful URLs:"
echo "  MLflow UI: http://localhost:5001"
echo "  API docs: http://localhost:8000/docs"
echo "  Health check: http://localhost:8000/health"
echo ""
echo "📁 Data: Audio files are in data/TRAIN/ with labels in data/TRAIN.csv (Kaggle format)"
echo "🔗 Dataset: https://www.kaggle.com/datasets/imsparsh/audio-speech-sentiment/data"
