# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

# Output value definitions

output "lambda_bucket_name" {
  description = "Name of the S3 bucket used to store function code."

  value = aws_s3_bucket.lambda_bucket.id
}

# API GATEWAY OUTPUTS
output "api_gateway_url" {
  value = aws_api_gateway_deployment.deploy.invoke_url
}

output "deployment_arn" {
  value = aws_api_gateway_deployment.deploy.execution_arn
}