resource "aws_api_gateway_rest_api" "rest_api" {
  name = "${var.rest_api_name}"
  endpoint_configuration {
    types = ["EDGE"]
  }
}

# TRAIN MODEL
resource "aws_api_gateway_resource" "train_model" {
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  parent_id   = aws_api_gateway_rest_api.rest_api.root_resource_id
  path_part   = "train_model"
}

resource "aws_api_gateway_method" "http_method" {
  authorization = "NONE"
  http_method   = "GET"
  resource_id   = aws_api_gateway_resource.train_model.id
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
}

# FTSE PREDICTIONS
resource "aws_api_gateway_resource" "ftse_predictions" {
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  parent_id   = aws_api_gateway_resource.pdf.id
  path_part   = "ftse_predictions"
}

resource "aws_api_gateway_method" "http_method" {
  authorization = "NONE"
  http_method   = "GET"
  resource_id   = aws_api_gateway_resource.ftse_predictions.id
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
}

#PREDICT NEXT DAY
resource "aws_api_gateway_resource" "predict_next_day" {
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  parent_id   = aws_api_gateway_rest_api.rest_api.root_resource_id
  path_part   = "predict_next_day"
}

resource "aws_api_gateway_method" "http_method" {
  authorization = "NONE"
  http_method   = "GET"
  resource_id   = aws_api_gateway_resource.gateway_resource.id
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
}

#PREDICT NEXT WEEK
resource "aws_api_gateway_resource" "predict_next_week" {
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  parent_id   = aws_api_gateway_resource.pdf.id
  path_part   = "predict_next_week"
}

resource "aws_api_gateway_method" "http_method" {
  authorization = "NONE"
  http_method   = "GET"
  resource_id   = aws_api_gateway_resource.gateway_resource.id
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
}

resource "aws_api_gateway_integration" "api_int" {
  http_method = aws_api_gateway_method.http_method.http_method
  resource_id = aws_api_gateway_resource.gateway_resource.id
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  integration_http_method = "POST"
  type        = "AWS_PROXY"
  uri         = "${var.lamda_arn}"
}

resource "aws_api_gateway_deployment" "deploy" {
  depends_on = [aws_api_gateway_integration.api_int]
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_rest_api.rest_api.body,
      aws_api_gateway_rest_api.rest_api.root_resource_id,
      aws_api_gateway_method.http_method.id,
      aws_api_gateway_integration.api_init.id,
    ]))
  }
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "stage" {
  deployment_id = aws_api_gateway_deployment.deploy.id
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
  stage_name    = "${var.stage_name}"
}

resource "aws_api_gateway_method_settings" "pdfcreate" {
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  stage_name  = aws_api_gateway_stage.stage.stage_name
  method_path = "create/POST"

  settings {
    data_trace_enabled = true
    metrics_enabled = true
    logging_level   = "INFO"
  }
}