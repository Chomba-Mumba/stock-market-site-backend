terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }
}

terraform {
  backend "s3" {
    bucket         = "stock-market-site-tfstate-bucket"
    key            = "terraform.tfstate"
    profile        = "assumed-role"
    region         = "eu-west-2"
    dynamodb_table = "terraform_stock_market_prediction_tflock"
    encrypt        = true
  }
}

provider "aws" {
  profile = "assumed-role"
  region  = "eu-west-2"
}

resource "aws_s3_bucket" "terraform_state_bucket" {
  bucket = "stock-market-site-tfstate-bucket"
}

resource "aws_s3_bucket_versioning" "versioning" {
  bucket = aws_s3_bucket.terraform_state_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "encryption" {
  bucket = aws_s3_bucket.terraform_state_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_dynamodb_table" "terraform_lock" {
  name         = "stock_market_prediction_tflock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }
}