ls -lh lambda/

echo "Zipping and uploading lambda functions..."
for dir in lambda/*; do
    if [ -d "$dir" ] && [ "$(basename "$dir")" != "predictions_lambda" ]; then
    zip_file="${dir}.zip"
    base_name="$(basename "$dir")"

    zip -r "$zip_file" "$dir"

    hash=$(sha256sum "$zip_file" | awk '{print $1}')

    aws s3 cp "$zip_file" "s3://stock-market-site/lambda/${base_name}.zip" \
        --metadata hash="$hash" \
        --metadata-directive REPLACE
    fi
done