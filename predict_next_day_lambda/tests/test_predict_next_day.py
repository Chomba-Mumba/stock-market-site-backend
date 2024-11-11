from io import StringIO
import tensorflow as tf
import pandas as pd
import numpy as np
import datetime
import logging
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

import boto3, os

import pytest
from moto import mock_aws

from predict_next_day_lambda.predict_next_day import lambda_handler, predict_next_day, scale_data, unscale_data

@mock_aws
def test_lambda_handler():
    s3 = boto3.client('s3', region_name='eu-west-1')
    bucket_name = "test-bucket"
    model_key = "test-key"
    pred_key = "predictions.csv"
    model_path = "tmp/mock_model.h5"
    pred_path = "tmp/predictions.csv"

    # Create the bucket
    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})

    # Create and save a simple model
    os.makedirs("tmp", exist_ok=True)
    model = create_simple_model()
    model.save(model_path)
    s3.upload_file(model_path, bucket_name, model_key)

    # Create and upload a mock predictions.csv file
    mock_data = pd.DataFrame({
        "Date": [pd.Timestamp("2024-11-11")],
        "Date + 1": [np.nan],
        "Date + 5": [np.nan]
    })
    mock_data.to_csv(pred_path, index=False)
    s3.upload_file(pred_path, bucket_name, pred_key)

    # Set up the event for the lambda_handler
    event = {
        'bucket_name': bucket_name,
        'model_key': model_key,
        'pred_key': pred_key,
        'local_path': model_path,
        'pred_path': pred_path
    }
    context = {}

    response = lambda_handler(event, context)

    assert response['statusCode'] == 200
    assert "Prediction completed and stored in S3." in response['body']

def create_simple_model():
    model = Sequential([
        LSTM(50, input_shape=(25, 2)),  # Input shape should match the sequence length and feature count
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model