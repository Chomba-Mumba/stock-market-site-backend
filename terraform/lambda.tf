data "aws_s3_bucket_object" "predictions_lambda_zip" {
  bucket = "stock-market-site"
  key = "lambda/predictions_lambda.zip"
}

# predictions Lambda
resource "aws_lambda_function" "predictions_lambda" {
  function_name = "predictions_lambda"
  role          = aws_iam_role.stock_market_lambda_role.arn
  handler       = "predictions_lambda.predictions.lambda_handler"

  runtime = "python3.9"

  s3_bucket  = "stock-market-site"
  s3_key     = "lambda/predictions_lambda.zip"
  depends_on = [aws_iam_role.stock_market_lambda_role]

  source_code_hash = data.aws_s3_bucket_object.predictions_lambda_zip.etag
}
resource "aws_cloudwatch_log_group" "predictions" {
  name = "/aws/lambda/${aws_lambda_function.predictions_lambda.function_name}"

  retention_in_days = 30
}