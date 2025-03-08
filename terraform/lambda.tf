# predictions Lambda
resource "aws_lambda_function" "predictions_lambda" {
  function_name = "predictions_lambda"
  role          = aws_iam_role.stock_market_lambda_role.arn
  handler       = "predictions_lambda.predictions.lambda_handler"

  runtime = "python3.9"
  memory_size   = 1024  
  timeout       = 60  

  depends_on = [aws_iam_role.stock_market_lambda_role]

  image_uri    = var.image_uri
  package_type = "Image"
}

resource "aws_cloudwatch_log_group" "predictions" {
  name = "/aws/lambda/${aws_lambda_function.predictions_lambda.function_name}"

  retention_in_days = 30
}