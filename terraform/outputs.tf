# Copyright (c) HashiCorp, Inc.
# SPDX-License-Identifier: MPL-2.0

# OUTPUT FUNCTION NAMES
output "predictions_function_name" {
  description = "Name of the predictions Lambda function."

  value = aws_lambda_function.predictions_lambda.function_name
}

# API GATEWAY OUTPUTS
output "api_gateway_url" {
  value = aws_api_gateway_deployment.stock_market_site_deploy.invoke_url
}

output "deployment_arn" {
  value = aws_api_gateway_deployment.stock_market_site_deploy.execution_arn
}