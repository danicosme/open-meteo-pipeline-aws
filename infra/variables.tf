variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "us-east-1"
}

variable "project" {
  description = "Project name for resource tagging"
  type        = string
  default     = "open-meteo-pipeline-aws"
}

variable "environment" {
  description = "Environment name for resource tagging"
  type        = string
  default     = "dev"
}

variable "lambda_runtime" {
  description = "Runtime for Lambda functions"
  type        = string
  default     = "python3.12"
}

variable "lambda_timeout" {
  description = "Timeout for Lambda functions in seconds"
  type        = number
  default     = 300
}

variable "lambda_memory" {
  description = "Memory allocation for Lambda functions in MB"
  type        = number
  default     = 1536
}

variable "sqs_visibility_timeout" {
  description = "Visibility timeout for SQS queues in seconds"
  type        = number
  default     = 300
}

variable "sqs_message_retention_days" {
  description = "Message retention period for SQS queues in days"
  type        = number
  default     = 7
}

variable "api_url" {
  description = "API URL for the application"
  type        = string
  default     = "https://api.open-meteo.com/v1/forecast"
}

variable "api_router_url" {
  description = "API Router URL for the text model"
  type        = string
  default     = "https://openrouter.ai/api/v1/chat/completions"
  
}

variable "model" {
  description = "Model for the text generation"
  type        = string
  default     = "deepseek/deepseek-r1-0528:free"
}

variable "openrouter_api_key" {
  description = "API key for OpenRouter"
  type        = string
  default     = "/open-meteo-pipeline-aws/openrouter_api_key"
}