#!/usr/bin/env python3
"""
Setup Verification Script for Audio Sentiment Analysis MLOps Project
"""

import os
import sys
import subprocess
import importlib
from pathlib import Path

def check_python_version():
    """Check Python version compatibility."""
    version = sys.version_info
    if version.major != 3 or version.minor < 9:
        print("❌ Python 3.9+ required. Current:", f"{version.major}.{version.minor}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_required_packages():
    """Check if required packages are installed."""
    required = [
        'librosa', 'scikit-learn', 'fastapi', 'uvicorn',
        'mlflow', 'prefect', 'evidently', 'pytest'
    ]
    
    missing = []
    for package in required:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"❌ {package}")
    
    return len(missing) == 0

def check_data_structure():
    """Check if data directory structure is correct."""
    data_path = Path('data/TRAIN')
    csv_file = data_path / 'TRAIN.csv'
    
    if not data_path.exists():
        print("❌ data/TRAIN directory not found")
        return False
    
    if not csv_file.exists():
        print("❌ data/TRAIN/TRAIN.csv not found")
        return False
    
    wav_files = list(data_path.glob('*.wav'))
    if len(wav_files) == 0:
        print("❌ No WAV files found in data/TRAIN/")
        return False
    
    print(f"✅ Data structure: {len(wav_files)} WAV files found")
    return True

def check_docker():
    """Check if Docker is available."""
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Docker not found or not running")
    return False

def check_aws_cli():
    """Check if AWS CLI is configured."""
    try:
        result = subprocess.run(['aws', 'sts', 'get-caller-identity'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ AWS CLI configured")
            return True
    except FileNotFoundError:
        pass
    
    print("⚠️  AWS CLI not configured (optional for local development)")
    return False

def main():
    """Run all verification checks."""
    print("🔍 Audio Sentiment Analysis MLOps Project - Setup Verification\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_required_packages),
        ("Data Structure", check_data_structure),
        ("Docker", check_docker),
        ("AWS CLI", check_aws_cli)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n📋 Checking {name}:")
        results.append(check_func())
    
    print("\n" + "="*50)
    passed = sum(results[:4])  # AWS CLI is optional
    total = 4
    
    if passed == total:
        print("🎉 All checks passed! Ready to run the MLOps pipeline.")
        print("\nNext steps:")
        print("1. python src/pipeline.py")
        print("2. python src/deployment/api.py &")
        print("3. curl -X POST -F 'file=@data/TRAIN/1.wav' http://localhost:8000/predict")
    else:
        print(f"❌ {total - passed} checks failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
