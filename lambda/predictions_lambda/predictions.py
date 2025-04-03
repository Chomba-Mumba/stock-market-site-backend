from io import StringIO
import tensorflow as tf
import pandas as pd
import numpy as np
import datetime
import logging

import boto3

from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from functools import wraps

from utils.load_data import load_past_data

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
        print("next_pred: ",next_prediction_scaled)
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

def predict_next_week(pred_path,model,train_df):
    try:

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

def predict_next_day(pred_path,train_df,model):
    try:
        # Create sequences for single-step model
        seq_length = 25
        num_of_features = 2
        
        print("train_df", train_df)
        df, scaler = scale_data(train_df)
        seq = np.array(df[-seq_length:]).reshape((1, seq_length, num_of_features))

        # Load the model
        next_day_pred = model.predict(seq)[0][0]

        # Inverse transform the prediction
        next_day_pred_scaled = np.array([[next_day_pred, next_day_pred]])
        next_day_pred_actual = scaler.inverse_transform(next_day_pred_scaled)[0][0]
        logger.info("Predicted stock price for the next day: %f", next_day_pred_actual)
        print("next1", next_day_pred_actual)
        # Load predictions file and update it
        print(pred_path)
        pred_df = pd.read_csv(pred_path)
        print(pred_df)
        pred_df.loc[pred_df['Date + 1'].isna().idxmax(), 'Date + 1'] = next_day_pred_actual

        return pred_df
    except FileNotFoundError as e:
        logger.error("File not found: %s", e)
        raise
    except Exception as e:
        logger.error("Error in prediction function: %s", e)
        raise

#Routes

@route_decorator('GET','/predict_next_week')
def predict_next_week_lambda(event,context):
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

    multi_model = load_model(multi_local_path)
    pred_df = predict_next_week(pred_path, multi_model,train_df)
    csv_buffer = StringIO()
    pred_df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=pred_key, Body=csv_buffer.getvalue())

    return {
        'statusCode': 200,
        'body': 'Prediction completed and stored in S3.'
    }
# //TODO - Incorporate multi-step model

@route_decorator('GET','/predict_next_day')
def predict_next_day_lambda(event,context):
    s3 = boto3.client('s3')

    bucket_name = event.get('bucket_name')

    local_path = event.get('local_path')
    pred_path = event.get('pred_path')

    model_key = event.get('model_key')
    pred_key = event.get('pred_key')

    if not bucket_name or not model_key or not pred_key:
        return {
            'statusCode': 400,
            'body': 'Missing one of the required parameters: bucket_name, model_key, pred_key'
        }

    #download model from s3 bucket.
    s3.download_file(bucket_name, model_key, local_path)
    s3.download_file(bucket_name, pred_key, pred_path)

    model = load_model(local_path)

    pred_df = predict_next_day(pred_path,train_df,model)
    csv_buffer = StringIO()
    pred_df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=pred_key, Body=csv_buffer.getvalue())

    return {
        'statusCode': 200,
        'body': 'Prediction completed and stored in S3.'
    }   

def lambda_handler(event,context):

    try:
        method = event.get('httpMethod')
        path = event.get('path')
        print(routes)
        print(f"{(method,path)}")

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
        'path': '/predict_next_week',
        'bucket_name': 'stock-market-site',
        'multi_local_path': '/tmp/multi_step_lstm_model.h5',
        'pred_path': '/tmp/predictions.csv',
        'multi_model_key': 'models/multi_step_lstm_model.h5',
        'pred_key': 'predictions/predictions.csv'
    }
    context = {}

    print(lambda_handler(event, context))

    event = {
        'httpMethod': 'GET',
        'path': '/predict_next_day',
        'bucket_name': 'stock-market-site',
        'local_path': '/tmp/lstm_model_38_0.03.h5',
        'pred_path': '/tmp/predictions.csv',
        'model_key': 'models/lstm_model_38_0.03.h5',
        'pred_key': 'predictions/predictions.csv'
    }

    print(lambda_handler(event, context))