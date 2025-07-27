output "ecr_repository_url" {
  description = "URL of the ECR repository"
  value       = aws_ecr_repository.app_repo.repository_url
}

output "ecr_repository_name" {
  description = "Name of the ECR repository"
  value       = aws_ecr_repository.app_repo.name
}

output "s3_model_bucket" {
  description = "Name of the S3 bucket for models"
  value       = aws_s3_bucket.model_bucket.bucket
}

output "s3_data_bucket" {
  description = "Name of the S3 bucket for data"
  value       = aws_s3_bucket.data_bucket.bucket
}

output "ecs_task_execution_role_arn" {
  description = "ARN of the ECS task execution role"
  value       = aws_iam_role.ecs_task_execution_role.arn
}

output "lambda_role_arn" {
  description = "ARN of the Lambda role"
  value       = aws_iam_role.lambda_role.arn
}

output "aws_region" {
  description = "AWS region"
  value       = var.aws_region
}

# ECS outputs commented out due to permission restrictions
# output "ecs_cluster_name" {
#   description = "Name of the ECS cluster"
#   value       = aws_ecs_cluster.main.name
# }

# output "ecs_cluster_arn" {
#   description = "ARN of the ECS cluster"
#   value       = aws_ecs_cluster.main.arn
# }
