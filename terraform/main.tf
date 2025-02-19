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
    dynamodb_table = "stock_market_prediction_tflock"
    encrypt        = true
  }
}

provider "aws" {
  profile = "assumed-role"
  region  = "eu-west-2"
}