#!/bin/bash

set -e  # Exit on any error

echo "🚀 Deploying Audio Sentiment Analysis Infrastructure to AWS..."

# Check if AWS CLI is configured
if ! aws sts get-caller-identity > /dev/null 2>&1; then
    echo "❌ AWS CLI not configured. Please run 'aws configure' first."
    exit 1
fi

# Check if Terraform is installed
if ! command -v terraform &> /dev/null; then
    echo "❌ Terraform not found. Please install Terraform first."
    exit 1
fi

echo "✅ AWS credentials and Terraform verified"

# Initialize Terraform
echo "📦 Initializing Terraform..."
terraform init

# Plan the deployment
echo "📋 Planning deployment..."
terraform plan -out=tfplan

# Apply the deployment
echo "🔨 Applying infrastructure changes..."
if terraform apply tfplan; then
    echo "✅ Infrastructure deployed successfully!"
    echo ""
    echo "📊 Infrastructure Details:"
    terraform output
    echo ""
    echo "🔧 Next Steps:"
    echo "1. Build and push Docker image to ECR:"
    echo "   aws ecr get-login-password --region $(terraform output -raw aws_region) | docker login --username AWS --password-stdin $(terraform output -raw ecr_repository_url)"
    echo "   docker build -t $(terraform output -raw ecr_repository_name) ."
    echo "   docker tag $(terraform output -raw ecr_repository_name):latest $(terraform output -raw ecr_repository_url):latest"
    echo "   docker push $(terraform output -raw ecr_repository_url):latest"
    echo ""
    echo "2. Deploy to ECS (manual step - see README for ECS task definition)"
else
    echo "❌ Deployment failed!"
    exit 1
fi
