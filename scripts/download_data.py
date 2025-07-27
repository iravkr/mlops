import os
import zipfile
import subprocess
import shutil
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_kaggle_data():
    """Download and extract audio sentiment dataset from Kaggle"""
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    zip_path = Path.home() / "Downloads" / "audio-speech-sentiment.zip"
    
    try:
        # Download using Kaggle API
        logger.info("Downloading dataset from Kaggle...")
        cmd = [
            "curl", "-L", "-o", str(zip_path),
            "https://www.kaggle.com/api/v1/datasets/download/imsparsh/audio-speech-sentiment"
        ]
        subprocess.run(cmd, check=True)
        
        # Extract the dataset
        logger.info("Extracting dataset...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(data_dir)
        
        # Clean up zip file
        zip_path.unlink()
        
        logger.info("Dataset downloaded and extracted to data/")
        
    except subprocess.CalledProcessError:
        logger.error("Failed to download dataset. Make sure you have Kaggle API access.")
        logger.info("Alternative: Download manually from https://www.kaggle.com/datasets/imsparsh/audio-speech-sentiment")
        create_sample_structure()
    except Exception as e:
        logger.error(f"Error: {e}")
        create_sample_structure()


def create_sample_structure():
    """Create sample directory structure matching Kaggle format"""
    
    data_dir = Path("data")
    train_dir = data_dir / "TRAIN"
    train_dir.mkdir(parents=True, exist_ok=True)
    
    # Create sample CSV file
    csv_file = data_dir / "TRAIN.csv"
    with open(csv_file, "w") as f:
        f.write("Filename,Class\n")
        f.write("# Download actual dataset from:\n")
        f.write("# https://www.kaggle.com/datasets/imsparsh/audio-speech-sentiment\n")
    
    readme_file = train_dir / "README.txt"
    with open(readme_file, "w") as f:
        f.write("Audio files (.wav) should be placed in this directory\n")
        f.write("Labels are in ../TRAIN.csv with format: Filename,Class\n")
        f.write("Download from: https://www.kaggle.com/datasets/imsparsh/audio-speech-sentiment\n")
    

def create_dummy_audio_files():
    """Create dummy audio files for testing purposes in correct format"""
    try:
        import numpy as np
        import soundfile as sf
        
        # Create dummy files in the correct TRAIN directory
        train_dir = Path("data/TRAIN")
        train_dir.mkdir(parents=True, exist_ok=True)
        
        # Create a few dummy audio files
        sample_rate = 22050
        duration = 3
        
        for i in range(3):
            # Generate random audio data
            audio_data = np.random.randn(sample_rate * duration) * 0.1
            filename = train_dir / f"{i+1}.wav"
            sf.write(filename, audio_data, sample_rate)
        
        logger.info("Dummy audio files created for testing")
    except ImportError:
        logger.warning("numpy/soundfile not installed, skipping dummy audio creation")


if __name__ == "__main__":
    download_kaggle_data()
    create_dummy_audio_files()
