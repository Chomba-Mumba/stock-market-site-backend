import logging
import boto3

from functools import wraps

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

@route_decorator('GET','/news_articles')
def news_articles():
    news_articles = "ewrer"
    return {
        'statusCode' : 200,
        'body' : news_articles
    }

@route_decorator('GET','/news_images')
def news_images():
    