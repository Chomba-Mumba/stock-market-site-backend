
variable "aws_region" {
  description = "AWS region for all resources."

  type    = string
  default = "eu-west-2"
}

#API GATEWAY VARIABLES

variable "rest_api_name" {
  description = "The name of your API"
  type        = string
  default     = "stock_market_prediction_api"
}

variable "rest_api_description" {
  description = "The name of your API"
  type        = string
  default     = "stock_market_prediction_api"
}

variable "stage_name" {
  description = "The name of your API stage"
  type        = string
  default     = "stock_market_prediction_stage"
}

# lambda_predictions image uri
variable "image_uri" {
  type      = string
  sensitive = true
}

variable "s3_bucket" {
  type = string
  default = "stock-market-site"
}