import tensorflow as tf
import os

import boto3

from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

from services.model_utils import load_past_data
from services.model_utils import create_sequences
from services.model_utils import create_sequences_multi

tf.config.run_functions_eagerly(True)

def split_scale_data():

    train_df = load_past_data()

    X_train, X_val, y_train, y_val = train_test_split(train_df[['Close-5', 'Close']], train_df['Future Close'], test_size=0.3, shuffle=False)

    scaler = MinMaxScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)

    y_scaler = MinMaxScaler()
    y_train = y_scaler.fit_transform(y_train.values.reshape(-1, 1))
    y_val = y_scaler.transform(y_val.values.reshape(-1, 1))

    return X_train, X_val, y_train, y_val

def train_models(local_path, multi_local_path):
    try:
        # Load and preprocess data
        X_train, X_val, y_train, y_val = split_scale_data()

        # Create sequences for single-step model
        seq_length = 25

        x_seq, y_seq  = create_sequences(X_train, y_train, seq_length)
        x_val_seq, y_val_seq  = create_sequences(X_train, y_train, seq_length)

        # Load the model
        model = load_model(local_path)

        # Train single step model first
        print(x_seq.shape)
        model.compile(optimizer='adam', loss='mean_absolute_error', metrics=['accuracy'], run_eagerly=True)

        model.fit(x_seq, y_seq, epochs=20, batch_size=8, validation_data = (x_val_seq, y_val_seq))

        # Train multi-step model
        X_train_multi, X_val_multi, y_train_multi, y_val_multi = split_scale_data()

        x_seq_multi, y_seq_multi  = create_sequences_multi(X_train_multi, y_train_multi, seq_length, 5)
        x_val_seq_multi, y_val_seq_multi  = create_sequences_multi(X_val_multi, y_val_multi, seq_length, 5)

        multi_model = load_model(multi_local_path)

        multi_model.compile(optimizer='adam', loss='mean_absolute_error', metrics=['accuracy'], run_eagerly=True)

        multi_model.fit(x_seq_multi, y_seq_multi, epochs=20, batch_size=8, validation_data = (x_val_seq_multi, y_val_seq_multi))

        model.save(local_path)
        multi_model.save(multi_local_path)
    except FileNotFoundError as e:
        print("File not found: ", e)
    except Exception as e:
        print("An error occurred: ", e)


def lambda_handler(event, context):
    # Load model form S3 bucket

    s3 = boto3.client('s3')
    bucket_name = event.get('bucket_name')

    model_key = event.get('model_key')
    multi_model_key =  event.get('multi_model_key')

    local_path = event.get('local_path')
    multi_local_path = event.get('multi_local_path')

    if not bucket_name or not model_key or not multi_model_key:
        return {
            'statusCode': 400,
            'body': 'Missing one of the required parameters: bucket_name, model_key, pred_key'
        }

    # Download model from S3 to /tmp
    s3.download_file(bucket_name, model_key, local_path)
    s3.download_file(bucket_name, multi_model_key, multi_local_path)

    # Train the models
    train_models(local_path, multi_local_path)

    # Upload the models to S3
    s3.upload_file(local_path, bucket_name, model_key)
    s3.upload_file(multi_local_path, bucket_name, multi_model_key)

