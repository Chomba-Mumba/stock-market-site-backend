from io import StringIO
import tensorflow as tf
import pandas as pd
import numpy as np
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

def predict_multiple_steps(sequence, model, scaler, seq_length, steps=1):
    # Convert sequence to a numpy array if it's a df
    if isinstance(sequence, pd.DataFrame):
        sequence = sequence.to_numpy()
        
    predictions = []
    
    for _ in range(steps):
        # Get the last `seq_length` rows to form the input sequence and reshape
        sequence_input = sequence[-seq_length:].reshape((1, seq_length, 2))
        
        # Predict the next timestep
        next_prediction_scaled = model.predict(sequence_input)[0][0]
        
        # Reshape and inverse transform to get the actual prediction
        next_prediction = scaler.inverse_transform([[next_prediction_scaled, next_prediction_scaled]])[0][0]
        predictions.append(next_prediction)
        
        # Update sequence to include the new scaled prediction and roll one step forward
        next_prediction_row = np.array([[sequence[-1, 0], next_prediction_scaled]])  # [Close-5, predicted Close]
        sequence = np.vstack([sequence[1:], next_prediction_row])  # Shift window to the next step

    return predictions

def scale_data(train_df):
    train_df_multi = train_df[['Close-5', 'Close']]
    scaler = MinMaxScaler()
    train_df_multi = scaler.fit_transform(train_df_multi)
    return train_df_multi, scaler

def unscale_data(scaler, data):
    return scaler.inverse_transform(data)



def predict_next_week(local_path, pred_path):
    try:
        # Load the model
        model = load_model(local_path)

        train_df_multi, scaler = scale_data(train_df)
        next_5_days_pred = predict_multiple_steps(train_df_multi, model, scaler=scaler, seq_length=25, steps=5)
        print("Predicted stock prices for the next 5 days:", next_5_days_pred)

        # save predictions in predictions.csv
        pred_df = pd.read_csv(pred_path)

        # Create new df to store predictions then concat
        new_dates = pd.date_range(start=datetime.date.today() + datetime.timedelta(days=1), periods=5).date
        new_data = pd.DataFrame({
            'Date': new_dates,
            'Date + 1': np.nan,
            'Date + 5': next_5_days_pred
        })

        pred_df = pd.concat([pred_df, new_data], ignore_index=True)

        return pred_df
    except FileNotFoundError as e:
        logger.error("File not found: %s", e)
        raise
    except Exception as e:
        logger.error("An error occurred: %s", e)
        raise

def lambda_handler(event,context):
    s3 = boto3.client('s3')

    # Load model from S3 bucker
    bucket_name = event.get('bucket_name')
    
    # Running on AWS Lambda
    multi_local_path = event.get('multi_local_path')
    pred_path = event.get('pred_path')

    multi_model_key =  event.get('multi_model_key')
    pred_key = event.get('pred_key')

    if not bucket_name or not multi_model_key or not pred_key:
        return {
            'statusCode': 400,
            'body': 'Missing one of the required parameters: bucket_name, model_key, pred_key'
        }
    
    # Download model from S3 to temp folder
    s3.download_file(bucket_name, multi_model_key, multi_local_path)
    s3.download_file(bucket_name, pred_key, pred_path)

    pred_df = predict_next_week(multi_local_path, pred_path)
    csv_buffer = StringIO()
    pred_df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=pred_key, Body=csv_buffer.getvalue())

    return {
        'statusCode': 200,
        'body': 'Prediction completed and stored in S3.'
    }
# //TODO - Incorporate mult-step model
