from io import StringIO
import tensorflow as tf
import pandas as pd
import numpy as np
import os
import datetime
import logging

import boto3

from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

from services.model_utils import load_past_data

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load stock data
try:
    train_df = load_past_data(per="3mo")
except Exception as e:
    logger.error("Failed to load data: %s", e)
    raise


def scale_data(train_df):
    train_df = train_df[['Close-5', 'Close']]
    scaler = MinMaxScaler()
    train_df = scaler.fit_transform(train_df)
    return train_df, scaler

def unscale_data(scaler, data):
    return scaler.inverse_transform(data)

train_df, scaler = scale_data(train_df)

def predict_next_day(local_path, pred_path):
    try:
        # Create sequences for single-step model
        seq_length = 25
        num_of_features = 2
        seq = np.array(train_df[-seq_length:]).reshape((1, seq_length, num_of_features))

        # Load the model
        model = load_model(local_path)
        next_day_pred = model.predict(seq)[0][0]

        # Inverse transform the prediction
        next_day_pred_scaled = np.array([[next_day_pred, next_day_pred]])
        next_day_pred_actual = scaler.inverse_transform(next_day_pred_scaled)[0][0]
        logger.info("Predicted stock price for the next day: %f", next_day_pred_actual)

        # Load predictions file and update it
        pred_df = pd.read_csv(pred_path)
        pred_df.loc[pred_df['Date + 1'].isna().idxmax(), 'Date + 1'] = next_day_pred_actual

        return pred_df
    except FileNotFoundError as e:
        logger.error("File not found: %s", e)
        raise
    except Exception as e:
        logger.error("Error in prediction function: %s", e)
        raise


# Load model form S3 bucket
bucket_name = 'stock-market-site'
s3 = boto3.client('s3')
if os.getenv('AWS_EXECUTION_ENV') is not None:
    # Running on AWS Lambda
    local_path = '/tmp/lstm_model_38_0.03.h5'
    pred_path = '/tmp/predictions.csv'

    model_key = 'models/lstm_model_38_0.03.h5'
    pred_key = 'output/predictions.csv'

    # Download model from S3 to temp folder
    s3.download_file(bucket_name, model_key, local_path)
    s3.download_file(bucket_name, pred_key, pred_path)

    pred_df = predict_next_day(local_path, pred_path)
    csv_buffer = StringIO()
    pred_df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=pred_key, Body=csv_buffer.getvalue())
else:
    # Running locally (on Windows)
    temp_dir = os.path.join(os.getcwd(), 'temp')
    os.makedirs(temp_dir, exist_ok=True)  # Create temp directory if it doesn't exist
    local_path = os.path.join(temp_dir, 'lstm_model_38_0.03.h5')
    pred_path = os.path.join(temp_dir, 'predictions.csv')

    pred_df = predict_next_day(local_path, pred_path)
    print(pred_df)

# //TODO - Incorporate mult-step model
