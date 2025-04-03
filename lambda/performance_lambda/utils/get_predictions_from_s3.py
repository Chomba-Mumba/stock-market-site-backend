import boto3
import pandas as pd

def get_metrics(bucket_name,file_key,local_path):
    
    s3 = boto3.client('s3')
    
    #get csv from s3 adn return last 30 days of data
    s3.download_file(bucket_name,file_key,local_path)

    df = pd.read_csv(local_path)

    return df