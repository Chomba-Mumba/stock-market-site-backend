import boto3
import csv
import io

def get_csv_from_s3(bucket_name, file_key):
    s3_client = boto3.client('s3')
    
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        content = response['Body'].read().decode('utf-8')
        
        csv_reader = csv.reader(io.StringIO(content))
        
        rows = [row for row in csv_reader]
        
        return rows
    except Exception as e:
        print(f"Error retrieving or processing the CSV file: {e}")
        return None

def lambda_handler(event, context):
    bucket_name = event.get('bucket_name')
    file_key = event.get('file_key')

    if not bucket_name or not file_key:
        return {
            'statusCode': 400,
            'body': 'Error: bucket_name and file_key must be provided in the event.'
        }
    
    rows = get_csv_from_s3(bucket_name, file_key)
    
    if rows is None:
        return {
            'statusCode': 500,
            'body': 'Error: failed to retrieve the CSV file from S3.'
        }
    
    return {
        'statusCode': 200,
        'body': rows    # Return the CSV data as the response body
    }
    

