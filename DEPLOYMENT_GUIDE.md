# 🚀 Complete Deployment Guide

## Prerequisites

1. **Python 3.9+** installed
2. **Docker** installed and running
3. **AWS CLI** configured (for cloud deployment)
4. **Git** for version control

## Quick Start (5 minutes)

```bash
# 1. Setup environment
chmod +x setup.sh
./setup.sh
source venv/bin/activate

# 2. Download dataset to data/TRAIN/ (see data/README.md)

# 3. Run complete pipeline
python src/pipeline.py

# 4. Test API
python src/deployment/api.py &
curl -X POST -F "file=@data/TRAIN/1.wav" http://localhost:8000/predict
```

## Local Development Stack

```bash
# Start all services
docker-compose up

# Services available:
# - API: http://localhost:8000
# - MLflow: http://localhost:5001
# - API Docs: http://localhost:8000/docs
```

## Cloud Deployment (AWS)

```bash
# 1. Configure AWS
aws configure

# 2. Deploy infrastructure
cd infrastructure
./deploy.sh

# 3. Deploy container
cd ..
./scripts/deploy_to_aws.sh
```

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Expected: 5 tests passing
```

## Troubleshooting

See README.md for detailed troubleshooting steps.
