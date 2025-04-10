import numpy as np
import boto3
import pandas as pd
  
def calculate_model_accuracy(bucket_name,file_key, local_path):

    s3 = boto3.client('s3')

    s3.download_file(bucket_name,file_key, local_path)

    df = pd.read_csv(local_path)

    actual = np.array(df['actual'].dropna())
    predicted = np.array(df['predicted'].dropna())

    residuals = actual - predicted

    mae = np.mean(np.abs(residuals))
    mse = np.mean(residuals ** 2)
    rmse = np.sqrt(mse)
    return {
        'MAE': round(mae, 4),
        'MSE': round(mse, 4),
        'RMSE': round(rmse, 4)
    }

def get_metrics(bucket_name,file_key,local_path):
    
    s3 = boto3.client('s3')
    
    #get csv from s3 adn return last 30 days of data
    s3.download_file(bucket_name,file_key,local_path)

    df = pd.read_csv(local_path)

    return df