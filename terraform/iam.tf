data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    resource = [
        var.s3_bucket_arn,
        "${var.s3_bucket_arn}/*"
    ]
    actions = [
        "sts:AssumeRole",
        "s3:GetObject",
        "s3:PutObject"
        ]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}