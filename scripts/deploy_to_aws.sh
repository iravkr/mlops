#!/bin/bash

set -e  # Exit on any error

echo "🚀 Deploying Audio Sentiment API to AWS..."

# Check if we're in the project root
if [ ! -f "requirements.txt" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Get ECR details from Terraform output
cd infrastructure
ECR_URL=$(terraform output -raw ecr_repository_url 2>/dev/null)
ECR_NAME=$(terraform output -raw ecr_repository_name 2>/dev/null)
AWS_REGION=$(terraform output -raw aws_region 2>/dev/null)
cd ..

if [ -z "$ECR_URL" ]; then
    echo "❌ No ECR repository found. Please run './infrastructure/deploy.sh' first."
    exit 1
fi

echo "✅ Found ECR repository: $ECR_URL"

# Login to ECR
echo "🔐 Logging into ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_URL

# Build Docker image
echo "🔨 Building Docker image..."
docker build -t $ECR_NAME .

# Tag for ECR
echo "🏷️  Tagging image for ECR..."
docker tag $ECR_NAME:latest $ECR_URL:latest

# Push to ECR
echo "📤 Pushing image to ECR..."
docker push $ECR_URL:latest

echo "✅ Docker image deployed to ECR successfully!"
echo ""
echo "🔧 Next Steps:"
echo "1. Create ECS task definition using the image: $ECR_URL:latest"
echo "2. Create ECS service to run the task"
echo "3. Configure load balancer (optional)"
echo ""
echo "📊 Image URI: $ECR_URL:latest"
