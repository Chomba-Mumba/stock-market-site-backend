#!/bin/bash
set -e

for dir in *_lambda; do
    if [ -d "$dir" ]; then
        LAMBDA_NAME="$dir"
        PACKAGE_DIR="lambda_dist_pkg"
        ZIP_FILE="lambda/${LAMBDA_NAME}.zip"

        #remove old pkg
        rm -rf ${PACKAGE_DIR}
        mkdir -p ${PACKAGE_DIR}

        #install deps
        pip install -r "$dir/requirements.txt" -t ${PACKAGE_DIR}

        #move the package directory
        cp -r ${PACKAGE_DIR}/* "$dir" 

        #create zip
        zip -r "${ZIP_FILE}" "$dir"

        echo "created lambda package: ${ZIP_FILE}"
    fi
done