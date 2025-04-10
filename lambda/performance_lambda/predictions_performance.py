import logging
import boto3
import json

from utils.calc_perf_metrics import calculate_model_accuracy, get_metrics

from functools import wraps

#setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

routes = {}

#decorator for request routing
def route_decorator(method,path):
    def decorator(func):
        routes[(method,path)] = func
        @wraps(func)

        def wrapper(*args,**kwargs):
            return func(*args,**kwargs)
        return wrapper
    return decorator

@route_decorator('GET','performance_metrics')
def performance_metrics(event,context):

    bucket_name = event['queryStringParameters'].get('bucket_name', '')
    local_path = event['queryStringParameters'].get('local_path', '')
    file_key = event['queryStringParameters'].get('file_key', '')

    if not local_path or not bucket_name or not file_key:
        return {
            'statusCode' : 400,
            'body' : 'Missing one of the required parameters: daily_returns, trade_returns'
        }
    
    performance = calculate_model_accuracy(bucket_name,file_key,local_path)

    return {
        'statusCode' : '200',
        'body' : json.dumps(performance)
    }

@route_decorator('GET','monthly_pred')
def monthly_pred_metrics(event,context):
    bucket_name = event['queryStringParameters'].get('bucket_name', '')
    local_path = event['queryStringParameters'].get('local_path', '')
    file_key = event['queryStringParameters'].get('file_key', '')
    print("received parameters frome event")
    if not local_path or not bucket_name or not file_key:
        return {
            'statusCode': 400,
            'body' : 'Missing one of the following required parameters: local_path, bucket_name, file_key'
        }
    
    #get csv from s3 adn return last 30 days of data
    df = get_metrics(bucket_name, file_key,local_path)
    print(df['predicted'].tail(30).tolist())
    return {
        'statusCode' : 200,
        'body' : json.dumps(df['predicted'].tail(30).tolist())
    }

@route_decorator('GET','monthly_values')
def monthly_values(event,context):

    bucket_name = event['queryStringParameters'].get('bucket_name', '')
    local_path = event['queryStringParameters'].get('local_path', '')
    file_key = event['queryStringParameters'].get('file_key', '')

    if not bucket_name or not local_path or not file_key:
        return {
            'statusCpode' : 400,
            'body' : 'Missing one of the following required arguments: bucket_name, local_path, file_key'
        }

    df = get_metrics(bucket_name, file_key,local_path)

    return {
        'statusCode' : 200,
        'body' : df[['predicted','actual']].dropna().tail(30).to_json()
    }

def lambda_handler(event,context):
    try:
        method = event.get('httpMethod')
        path = event.get('pathParameters', {}).get('proxy')

        if (method,path) in routes:
            return routes[(method,path)](event,context)
        else:
            return {
                'statusCode' : 404,
                'body': 'Endpoint not found'
            }
    except Exception as e:
        return {
            'statusCode' : 500,
            'body' : f'error: {str(e)}'
        }

if __name__ == "__main__":
    event = {
        'httpMethod' : 'GET',
        'path' : '/performance_metrics',
        'bucket_name' : 'stock-market-site',
        'local_path' : '/tmp/predictions.csv',
        'file_key' : 'predictions/predictions.csv'
    }
    context = {}
    print(lambda_handler(event,context))

    event = {
        'httpMethod' : 'GET',
        'path' : '/monthly_pred',
        'bucket_name' : 'stock-market-site',
        'local_path' : '/tmp/predictions.csv',
        'file_key' : 'predictions/predictions.csv'
    }
    print(lambda_handler(event,context))

    event = {
        'httpMethod' : 'GET',
        'path' : '/monthly_values',
        'bucket_name' : 'stock-market-site',
        'local_path' : '/tmp/predictions.csv',
        'file_key' : 'predictions/predictions.csv'
    }
    print(lambda_handler(event,context))
    