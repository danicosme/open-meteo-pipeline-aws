data "aws_ssm_parameter" "openrouter_api_key" {
  name = var.openrouter_api_key
}
