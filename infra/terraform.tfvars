aws_region = "us-east-1"
project     = "open-meteo-pipeline-aws"
environment = "dev"

lambda_runtime    = "python3.12"
lambda_timeout    = 300
lambda_memory     = 1536

sqs_visibility_timeout      = 300
sqs_message_retention_days  = 7
