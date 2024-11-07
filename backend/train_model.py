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

# Load model form S3 bucket

s3 = boto3.client('s3')
bucket_name = 'stock-market-site'

if os.getenv('AWS_EXECUTION_ENV') is not None:
    # Running on AWS Lambda
    local_path = '/tmp/lstm_model_38_0.03.h5'
    multi_local_path = '/tmp/multi_step_lstm_model.h5'
else:
    # Running locally (on Windows)
    temp_dir = os.path.join(os.getcwd(), 'temp')
    os.makedirs(temp_dir, exist_ok=True)  # Create temp directory if it doesn't exist
    local_path = os.path.join(temp_dir, 'lstm_model_38_0.03.h5')
    multi_local_path = os.path.join(temp_dir, 'multi_step_lstm_model.h5')

model_key = 'models/lstm_model_38_0.03.h5'
multi_model_key =  'models/multi_step_lstm_model.h5'

# Load and preprocess data

X_train, X_val, y_train, y_val = split_scale_data()

# Create sequences for single-step model
seq_length = 25
num_of_features = 2

x_seq, y_seq  = create_sequences(X_train, y_train, seq_length)
x_val_seq, y_val_seq  = create_sequences(X_train, y_train, seq_length)

# Download model from S3 to /tmp
s3.download_file(bucket_name, model_key, local_path)
s3.download_file(bucket_name, multi_model_key, multi_local_path)

# Load the model
model = load_model(local_path)

# Train single step model first
print(x_seq.shape)
model.compile(optimizer='adam', loss='mean_absolute_error', metrics=['accuracy'], run_eagerly=True)

model.fit(x_seq, y_seq, epochs=2, batch_size=8, validation_data = (x_val_seq, y_val_seq))

# Train multi-step model
X_train_multi, X_val_multi, y_train_multi, y_val_multi = split_scale_data()

# Create sequences for multi-step model
seq_length = 25
num_of_features = 2

x_seq_multi, y_seq_multi  = create_sequences_multi(X_train_multi, y_train_multi, seq_length, 5)
x_val_seq_multi, y_val_seq_multi  = create_sequences_multi(X_val_multi, y_val_multi, seq_length, 5)

multi_model = load_model(multi_local_path)

multi_model.compile(optimizer='adam', loss='mean_absolute_error', metrics=['accuracy'], run_eagerly=True)

multi_model.fit(x_seq_multi, y_seq_multi, epochs=2, batch_size=8, validation_data = (x_val_seq_multi, y_val_seq_multi))

model.save(local_path)
multi_model.save(multi_local_path)

# Upload the models to S3
s3.upload_file(local_path, bucket_name, model_key)
s3.upload_file(multi_local_path, bucket_name, multi_model_key)