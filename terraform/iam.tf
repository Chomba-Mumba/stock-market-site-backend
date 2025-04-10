
resource "aws_iam_role" "stock_market_lambda_role" {
  name = "stock_market_lambda_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_iam_policy_to_iam_role" {
  role       = aws_iam_role.stock_market_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "attach_ecr_readonly_policy" {
  role       = aws_iam_role.stock_market_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
}

resource "aws_iam_role_policy_attachment" "attach_lambda_s3_access" {
  role       = aws_iam_role.stock_market_lambda_role.name
  policy_arn = aws_iam_policy.lambda_s3_access.arn
}

data "aws_iam_policy_document" "lambda_s3_access" {
  statement {
    sid = "ReadWriteOnModelsAndPredictions"
    actions = [
      "s3:GetObject",
      "s3:PutObject"
    ]
    resources = [
      "arn:aws:s3:::stock-market-site/models/*",
      "arn:aws:s3:::stock-market-site/predictions/*"
    ]
  }
}

resource "aws_iam_policy" "lambda_s3_access" {
  name        = "lambda_s3_access"
  description = "Allow Lambda to Get/Put objects in stock-market-site bucket"
  policy      = data.aws_iam_policy_document.lambda_s3_access.json
}