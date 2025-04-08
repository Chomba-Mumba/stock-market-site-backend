from functools import wraps
from utils.news import get_ftse100_news
import json

import logging

#setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

routes = {}

#decorator for request routing
def route_decorator(method,path):
    def decorator(func):# wrap function at definition
        routes[(method,path)] = func
        @wraps(func)

        def wrapper(*args,**kwargs): #wrap function at runtime
            return func(*args,**kwargs)
        return wrapper
        
    return decorator

@route_decorator('GET','get_news_articles')
def get_news_articles(event,context):
    news_feed = get_ftse100_news()
    print(news_feed)

    if not news_feed:
        return {
            'statusCode' : 500,
            'body' : f'Failed to fetch news feed: {news_feed.status_code} - {news_feed.text}'
        }
    return {
        'statusCode': 200,
        'body': json.dumps(news_feed['feed']), 
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }

def lambda_handler(event,context):
    try:
        method = event.get('httpMethod')
        path = event.get('pathParameters', {}).get('proxy')

        if (method,path) in routes:
            return routes[(method,path)](event,context)
        else:
            return {
                'statusCode': 404,
                'body': 'Endpoint not found'
        }
    except Exception as e:
        return {
            'statusCode' : 500,
            'body' : f'error: {str(e)}'
        }

if __name__ == "__main__":
    event = {
        'httpMethod': 'GET',
        'path': 'get_news_articles'
    }
    context = {}
    print(lambda_handler(event,context))