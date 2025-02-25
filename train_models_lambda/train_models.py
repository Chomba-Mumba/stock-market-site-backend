
def lambda_handler(event, context):
    bucket_name = event.get('bucket_name')
    file_key = event.get('file_key')

    if not bucket_name or not file_key:
        return {
            'statusCode': 400,
            'body': 'Error: bucket_name and file_key must be provided in the event.'
        }

