#!/bin/bash
set -e

LAYER_PATH="lambda/layers/predictions_layer"

mkdir -p "${LAYER_PATH}/python"

#create layers zip
pip install -r requirements.txt -t "${LAYER_PATH}/python"

zip -r "${LAYER_PATH}.zip" "${LAYER_PATH}"

echo "Zipped Lambda Layer ${LAYER_PATH}"

#zip lambda functions
for dir in *_lambda; do
    if [ -d "$dir" ]; then
        LAMBDA_NAME="$dir"
        ZIP_FILE="lambda/${LAMBDA_NAME}.zip"
        #create zip
        zip -r "${ZIP_FILE}" "$dir"

        echo "created lambda package: ${ZIP_FILE}"
    fi
done

#upload lambda layers.
echo "uploading lambda layers..."

for zip_layer in lambda/layers*.zip do
    echo "$zip_layer"
    aws s3 cp "$zip_layer" "s3://stock-market-site/lambda/layers/$(basename "$zip_layer")"
done