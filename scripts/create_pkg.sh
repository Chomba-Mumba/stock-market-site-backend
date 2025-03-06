#!/bin/bash
set -e

export ECR_REPOSITORY=${ECR_REPOSITORY}

cd "predictions_lambda/"

echo "building  docker image... in $(pwd)"
ls -a

#build and tag image
docker build -t "stock_market_prediction/lambda_functions/predictions:latest" .

echo "pushing docker image to ecr: predictions"

# Push the image to ECR
docker push "stock_market_prediction/lambda_functions/predictions:latest"

echo "finished pushing docker image"

