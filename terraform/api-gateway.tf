resource "aws_api_gateway_rest_api" "stock_market_site_rest_api" {
  name        = var.rest_api_name
  description = var.rest_api_description

  endpoint_configuration {
    types = ["EDGE"]
  }
}

# PREDICT NEXT DAY Resource
resource "aws_api_gateway_resource" "predictions" {
  rest_api_id = aws_api_gateway_rest_api.stock_market_site_rest_api.id
  parent_id   = aws_api_gateway_rest_api.stock_market_site_rest_api.root_resource_id
  path_part   = "predictions"
}

resource "aws_api_gateway_method" "predictions_method" {
  authorization = "NONE"
  http_method   = "GET"
  resource_id   = aws_api_gateway_resource.predictions.id
  rest_api_id   = aws_api_gateway_rest_api.stock_market_site_rest_api.id
}

resource "aws_api_gateway_integration" "predictions_integration" {
  http_method             = aws_api_gateway_method.predictions_method.http_method
  resource_id             = aws_api_gateway_resource.predictions.id
  rest_api_id             = aws_api_gateway_rest_api.stock_market_site_rest_api.id
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.predictions_lambda.invoke_arn
}


resource "aws_api_gateway_deployment" "stock_market_site_deploy" {
  depends_on = [
    aws_api_gateway_integration.predictions_method_integration,
  ]

  rest_api_id = aws_api_gateway_rest_api.stock_market_site_rest_api.id
  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_method.predictions_method.id,
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "stage" {
  deployment_id = aws_api_gateway_deployment.stock_market_site_deploy.id
  rest_api_id   = aws_api_gateway_rest_api.stock_market_site_rest_api.id
  stage_name    = var.stage_name
}

# Lambda Permissions

resource "aws_lambda_permission" "predictions_permission" {
  statement_id  = "AllowAPIGatewayInvokePredictNextWeek"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.predictions_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.stock_market_site_rest_api.execution_arn}/*"
}

# api gateway proxy integration
resource "aws_api_gateway_resource" "proxy"{
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id = aws_api_gateway_rest_api.api.root_resource_id
  path_part = "{proxy+}" 
}

resource "aws_api_gateway_method" "proxy_method"{
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.proxy.id
  http_method = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "proxy_integration"{
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.proxy.id
  http_method = aws_api_gateway_method.proxy_method.http_method
  type = "AWS_PROXY"
  integration_http_method = "POST"
  uri = aws_lambda_function.lambda.invoke_arn
}