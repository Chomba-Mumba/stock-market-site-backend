#!/bin/bash
set -e

export ECR_REPOSITORY=${ECR_REPOSITORY}

cd "predictions_lambda/"

echo "building  docker image..."

#build image
docker build -t predictions .

#tag image
docker tag "predictions" "${ECR_REPOSITORY}/predictions:latest"

echo "pushing docker image to ecr: predictions"

# Push the image to ECR
docker push ${ECR_REPOSITORY}/predictions:latest

echo "finished pushing docker image"

