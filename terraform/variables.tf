
variable "aws_region" {
  description = "AWS region for all resources."

  type    = string
  default = "eu-west-2"
}

variable "s3_bucket_arn" {
  description = "ARN of the S3 bucket to store the lambda function code."

  type = string
}

#API GATEWAY VARIABLES

variable "rest_api_name" {
  description = "The name of your API"
  type        = string
  default     = "stock-market-prediction-api"
}

variable "rest_api_description" {
  description = "The name of your API"
  type        = string
  default     = "stock-market-prediction-api"
}

variable "stage_name" {
  description = "The name of your API stage"
  type        = string
  default     = "stock-market-prediction-stage"