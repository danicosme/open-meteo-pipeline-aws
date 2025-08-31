# output "raw_bucket" {
#   description = "Name of the raw data bucket"
#   value       = aws_s3_bucket.raw.id
# }

# output "processed_bucket" {
#   description = "Name of the processed data bucket"
#   value       = aws_s3_bucket.processed.id
# }

# output "enriched_bucket" {
#   description = "Name of the enriched data bucket"
#   value       = aws_s3_bucket.enriched.id
# }

# output "processed_queue_url" {
#   description = "URL of the SQS queue for processed data"
#   value       = aws_sqs_queue.processed.url
# }

# output "enriched_queue_url" {
#   description = "URL of the SQS queue for enriched data"
#   value       = aws_s3_bucket.enriched.url
# }

# output "lambda_role_arn" {
#   description = "ARN of the IAM role used by Lambda functions"
#   value       = aws_iam_role.lambda_role.arn
# }

# output "athena_workgroup" {
#   description = "Name of the Athena workgroup"
#   value       = aws_athena_workgroup.open_meteo.name
# }

# output "glue_database" {
#   description = "Name of the Glue database"
#   value       = aws_glue_catalog_database.open_meteo_processed.name
# }
