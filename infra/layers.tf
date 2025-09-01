# Lambda Layers
resource "aws_lambda_layer_version" "loguru" {
  filename                 = "../layers/loguru.zip"
  layer_name               = "loguru-x86_64"
  description              = "Loguru library for structured logging version 0.7.3"
  compatible_runtimes      = ["python3.12"]
  compatible_architectures = ["x86_64"]
}

resource "aws_lambda_layer_version" "python_dotenv" {
  filename                 = "../layers/python-dotenv.zip"
  layer_name               = "python-dotenv-x86_64"
  description              = "Python-dotenv for environment variables management version 1.1.0"
  compatible_runtimes      = ["python3.12"]
  compatible_architectures = ["x86_64"]
}

resource "aws_lambda_layer_version" "polars" {
  filename                 = "../layers/polars.zip"
  layer_name               = "polars-x86_64"
  description              = "Polars for data manipulation version 1.31.0"
  compatible_runtimes      = ["python3.12"]
  compatible_architectures = ["x86_64"]
}
