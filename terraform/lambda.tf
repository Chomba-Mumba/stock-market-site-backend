# predictions Lambda
resource "aws_lambda_function" "predictions_lambda" {
  function_name = "predictions_lambda"
  role          = aws_iam_role.stock_market_lambda_role.arn
  handler       = "predictions_lambda.predictions.lambda_handler"

  runtime = "python3.9"

  s3_bucket  = "stock-market-site"
  s3_key     = "lambda/predictions_lambda.zip"
  depends_on = [aws_iam_role.stock_market_lambda_role]

  layers = [aws_lambda_layer_version.predictions_layer.arn, aws_lambda_layer_version.predictions_layer]

  source_code_hash = filesha256("lambda/predictions_lambda.zip")
}

resource "aws_lambda_layer_version" "predictions_layer" {
  layer_name = "stock_market_predictions_layer"

  s3_bucket  = "stock-market-site"
  s3_key     = "lambda/layers/predictions_layer.zip"

  compatible_runtimes = ["python3.9"]
}

resource "aws_cloudwatch_log_group" "predictions" {
  name = "/aws/lambda/${aws_lambda_function.predictions_lambda.function_name}"

  retention_in_days = 30
}