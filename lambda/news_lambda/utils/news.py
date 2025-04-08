import requests
import random
import boto3

BASE_URL = 'https://www.alphavantage.co/query'

def get_ftse100_news():
    params = {
        'function': 'NEWS_SENTIMENT',
        'tickers': 'AAPL',
        'apikey': API_KEY,
        'limit': 5,
        'sort': 'LATEST'
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        feed = data.get('feed', [])
        if not feed:
            print("No news articles found.")
        else:
            return data
    else:
        return response

def get_news_images(bucket_name, file_key, local_path):
    

    s3 = boto3.client('s3')

    for _ in range(5): 
        #for each news article pulled use a radnom image
        image = random.randint(1,10)
        s3.download_file(bucket_name, str(image)+'.jpg',local_path)
        s3.download_file

