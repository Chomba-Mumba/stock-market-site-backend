
# FTSE predictions Lambda
resource "aws_lambda_function" "ftse_predictions_lambda" {
  function_name = "ftse_predictions_lambda"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "ftse_predictions_lambda.ftse_predictions_lambda.lambda_handler"

  runtime = "python3.11"

  s3_bucket     = "stock-market-site"
  s3_key        = "lambda/ftse_predictions_lambda.zip"
}

# Predict Next Day Lambda
resource "aws_lambda_function" "predict_next_day_lambda" {
  function_name = "predict_next_day_lambda"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "predict_next_day_lambda.predict_next_day_lambda.lambda_handler"

  runtime = "python3.11"

  s3_bucket     = "stock-market-site"
  s3_key        = "lambda/predict_next_day_lambda.zip"
}

# Predict Next Week Lambda
resource "aws_lambda_function" "predict_next_week_lambda" {
  function_name = "predict_next_week_lambda"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "predict_next_week_lambda.predict_next_week_lambda.lambda_handler"

  runtime = "python3.11"

  s3_bucket     = "stock-market-site"
  s3_key        = "lambda/predict_next_week_lambda.zip"
}