# S3 Buckets
resource "aws_s3_bucket" "raw" {
  bucket = "${var.project}-raw"
  tags   = local.common_tags
}

resource "aws_s3_bucket" "processed" {
  bucket = "${var.project}-processed"
  tags   = local.common_tags
}

resource "aws_s3_bucket" "enriched" {
  bucket = "${var.project}-enriched"
  tags   = local.common_tags
}

# S3 Bucket configurations
resource "aws_s3_bucket_server_side_encryption_configuration" "raw" {
  bucket = aws_s3_bucket.raw.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "processed" {
  bucket = aws_s3_bucket.processed.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "enriched" {
  bucket = aws_s3_bucket.enriched.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "raw" {
  bucket = aws_s3_bucket.raw.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "processed" {
  bucket = aws_s3_bucket.processed.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "enriched" {
  bucket = aws_s3_bucket.enriched.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# SQS Queues and Dead Letter Queues
resource "aws_sqs_queue" "processed_dlq" {
  name = "${var.project}-processed-dlq"
  tags = local.common_tags
}

resource "aws_sqs_queue" "enriched_dlq" {
  name = "${var.project}-enriched-dlq"
  tags = local.common_tags
}

resource "aws_sqs_queue" "processed" {
  name                       = "${var.project}-processed"
  visibility_timeout_seconds = var.sqs_visibility_timeout
  message_retention_seconds  = var.sqs_message_retention_days * 24 * 60 * 60
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.processed_dlq.arn
    maxReceiveCount     = 3
  })
  tags = local.common_tags
}

resource "aws_sqs_queue" "enriched" {
  name                       = "${var.project}-enriched"
  visibility_timeout_seconds = var.sqs_visibility_timeout
  message_retention_seconds  = var.sqs_message_retention_days * 24 * 60 * 60
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.enriched_dlq.arn
    maxReceiveCount     = 3
  })
  tags = local.common_tags
}

# Athena Workgroup
resource "aws_athena_workgroup" "open_meteo" {
  name = "${var.project}-workgroup"

  configuration {
    enforce_workgroup_configuration = true
    result_configuration {
      output_location = "s3://${aws_s3_bucket.processed.bucket}/athena-results/"
    }
  }

  tags = local.common_tags
}

# Glue Database
resource "aws_glue_catalog_database" "open_meteo_processed" {
  name = "open_meteo_processed"
}

# Glue Tables
resource "aws_glue_catalog_table" "weather" {
  name          = "tb_weather"
  database_name = aws_glue_catalog_database.open_meteo_processed.name

  table_type = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL       = "TRUE"
    classification = "parquet"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.processed.bucket}/weather/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"
    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
    }

    columns {
      name = "latitude"
      type = "double"
    }
    columns {
      name = "longitude"
      type = "double"
    }
    columns {
      name = "generationtime_ms"
      type = "double"
    }
    columns {
      name = "utc_offset_seconds"
      type = "int"
    }
    columns {
      name = "timezone"
      type = "string"
    }
    columns {
      name = "timezone_abbreviation"
      type = "string"
    }
    columns {
      name = "elevation"
      type = "double"
    }
    columns {
      name = "state"
      type = "string"
    }
    columns {
      name = "city"
      type = "string"
    }
    columns {
      name = "extraction_datetime"
      type = "timestamp"
    }
  }

  partition_keys {
    name = "state"
    type = "string"
  }
}

resource "aws_glue_catalog_table" "weather_hourly" {
  name          = "tb_weather_hourly"
  database_name = aws_glue_catalog_database.open_meteo_processed.name

  table_type = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL       = "TRUE"
    classification = "parquet"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.processed.bucket}/weather_hourly/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"
    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
    }

    columns {
      name = "latitude"
      type = "double"
    }
    columns {
      name = "longitude"
      type = "double"
    }
    columns {
      name = "time"
      type = "timestamp"
    }
    columns {
      name = "temperature_2m"
      type = "double"
    }
    columns {
      name = "relative_humidity_2m"
      type = "double"
    }
    columns {
      name = "windspeed_10m"
      type = "double"
    }
    columns {
      name = "precipitation"
      type = "double"
    }
    columns {
      name = "state"
      type = "string"
    }
    columns {
      name = "city"
      type = "string"
    }
    columns {
      name = "extraction_datetime"
      type = "timestamp"
    }
  }

  partition_keys {
    name = "year"
    type = "string"
  }
  partition_keys {
    name = "month"
    type = "string"
  }
  partition_keys {
    name = "day"
    type = "string"
  }
  partition_keys {
    name = "hour"
    type = "string"
  }
}

resource "aws_glue_catalog_table" "weather_hourly_units" {
  name          = "tb_weather_hourly_units"
  database_name = aws_glue_catalog_database.open_meteo_processed.name

  table_type = "EXTERNAL_TABLE"

  parameters = {
    EXTERNAL       = "TRUE"
    classification = "parquet"
  }

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.processed.bucket}/weather_hourly_units/"
    input_format  = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat"
    ser_de_info {
      serialization_library = "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
    }

    columns {
      name = "time"
      type = "string"
    }
    columns {
      name = "temperature_2m"
      type = "string"
    }
    columns {
      name = "relative_humidity_2m"
      type = "string"
    }
    columns {
      name = "windspeed_10m"
      type = "string"
    }
    columns {
      name = "precipitation"
      type = "string"
    }
    columns {
      name = "extraction_datetime"
      type = "timestamp"
    }
  }
}

# IAM Role for Lambda functions
resource "aws_iam_role" "lambda_role" {
  name = "${var.project}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = local.common_tags
}

# IAM Policy for Lambda functions
resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.project}-lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.raw.arn,
          "${aws_s3_bucket.raw.arn}/*",
          aws_s3_bucket.processed.arn,
          "${aws_s3_bucket.processed.arn}/*",
          aws_s3_bucket.enriched.arn,
          "${aws_s3_bucket.enriched.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "sqs:SendMessage",
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ]
        Resource = [
          aws_sqs_queue.processed.arn,
          aws_sqs_queue.enriched.arn,
          aws_sqs_queue.processed_dlq.arn,
          aws_sqs_queue.enriched_dlq.arn
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "athena:StartQueryExecution",
          "athena:GetQueryExecution",
          "athena:GetQueryResults",
          "glue:GetTable",
          "glue:GetPartition"
        ]
        Resource = [
          aws_athena_workgroup.open_meteo.arn,
          aws_glue_catalog_database.open_meteo_processed.arn,
          "${aws_glue_catalog_database.open_meteo_processed.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# Lambda functions
resource "aws_lambda_function" "ingestion" {
  filename      = "./app/src/ingestion/ingestion.zip"
  function_name = "${var.project}-ingestion"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = var.lambda_runtime
  timeout       = var.lambda_timeout
  memory_size   = var.lambda_memory

  environment {
    variables = {
      RAW_BUCKET          = aws_s3_bucket.raw.id
      PROCESSED_QUEUE_URL = aws_sqs_queue.processed.url
    }
  }

  tags = local.common_tags
}

resource "aws_lambda_function" "processing" {
  filename      = "./app/src/processing/processing.zip"
  function_name = "${var.project}-processing"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = var.lambda_runtime
  timeout       = var.lambda_timeout
  memory_size   = var.lambda_memory

  environment {
    variables = {
      RAW_BUCKET         = aws_s3_bucket.raw.id
      PROCESSED_BUCKET   = aws_s3_bucket.processed.id
      ENRICHED_QUEUE_URL = aws_sqs_queue.enriched.url
    }
  }

  tags = local.common_tags
}

resource "aws_lambda_function" "enrichment" {
  filename      = "./app/src/enrichment/enrichment.zip"
  function_name = "${var.project}-enrichment"
  role          = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = var.lambda_runtime
  timeout       = var.lambda_timeout
  memory_size   = var.lambda_memory

  environment {
    variables = {
      PROCESSED_BUCKET = aws_s3_bucket.processed.id
      ENRICHED_BUCKET  = aws_s3_bucket.enriched.id
    }
  }

  tags = local.common_tags
}

# Lambda SQS triggers
resource "aws_lambda_event_source_mapping" "processing_trigger" {
  event_source_arn = aws_sqs_queue.processed.arn
  function_name    = aws_lambda_function.processing.arn
  batch_size       = 1
}

resource "aws_lambda_event_source_mapping" "enrichment_trigger" {
  event_source_arn = aws_sqs_queue.enriched.arn
  function_name    = aws_lambda_function.enrichment.arn
  batch_size       = 1
}
