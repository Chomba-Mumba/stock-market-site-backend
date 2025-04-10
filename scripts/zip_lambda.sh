ls -lh lambda/

echo "Zipping and uploading lambda functions..."
for dir in ./*; do
    if [ -d "$dir" ] && [ "$(basename "$dir")" != "predictions_lambda" ]; then
    zip_file="${dir}.zip"
    base_name="$(basename "$dir")"
    echo "dir: $dir zip: $zip_file"
    cd "$dir"
    ls
    zip -r "../$zip_file" * #Zip everything in file

    cd ../

    hash=$(sha256sum "$zip_file" | awk '{print $1}')

    aws s3 cp "$zip_file" "s3://stock-market-site/lambda/${base_name}.zip" \
        --metadata hash="$hash" \
        --metadata-directive REPLACE
    fi
done