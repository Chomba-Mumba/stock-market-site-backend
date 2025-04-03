# predictions Lambda
resource "aws_lambda_function" "predictions_lambda" {
  function_name = "predictions_lambda"
  role          = aws_iam_role.stock_market_lambda_role.arn

  memory_size = 1024
  timeout     = 60

  depends_on = [aws_iam_role.stock_market_lambda_role]

  image_uri    = var.image_uri
  package_type = "Image"
}

resource "aws_cloudwatch_log_group" "predictions" {
  name = "/aws/lambda/${aws_lambda_function.predictions_lambda.function_name}"

  retention_in_days = 30
}

#performance lambda
data "aws_s3_object" "performance_lambda_object" {
  bucket = var.s3_bucket
  key = "lambda/performance_lambda.zip"
}

resource "aws_lambda_function" "performance_lambda" {
  function_name = "performance_lambda"

  handler = "performance_lambda.lambda_handler"
  runtime = "python3.11.9"
  role = aws_iam_role.stock_market_lambda_role.arn

  memory_size = 128
  timeout = 10

  depends_on = [aws_iam_role.stock_market_lambda_role]

  s3_bucket = var.s3_bucket
  s3_key = data.aws_s3_object.performance_lambda_object.key
  source_code_hash = data.aws_s3_object.performance_lambda_object.metadata.hash
}

resource "aws_cloudwatch_log_group" "performance" {
  name = "/aws/lambda/${aws_lambda_function.performance_lambda.function_name}"
  retention_in_days = 30
}

#news lambda
data "aws_s3_object" "news_lambda_object" {
  bucket = var.s3_bucket
  key = "lambda/news_lambda.zip"
}

resource "aws_lambda_function" "news_lambda" {
  function_name = "news_lambda"
  runtime = "python3.11.9"

  handler = "news_lambda.lambda_handler"

  role = aws_iam_role.stock_market_lambda_role.arn 

  memory_size = 128
  timeout = 10

  depends_on = [aws_iam_role.stock_market_lambda_role]

  s3_bucket = var.s3_bucket
  s3_key = data.aws_s3_object.news_lambda_object.key
  source_code_hash = data.aws_s3_object.news_lambda_object.metadata.hash
}

resource "aws_cloudwatch_log_group" "news" {
  name = "/aws/lambda/${aws_lambda_function.news_lambda.function_name}"
  retention_in_days = 30
}