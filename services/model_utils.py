"""
data_processing.py

This module provides functions for loading and preprocessing data 
for training and prediction tasks in the stock market Lambda functions.

Functions:
    - load_training_data: Loads and returns raw training data from a data source.
    - preprocess_data: Cleans and prepares data for model training or prediction.

Usage:
    Import this module to use data loading and preprocessing utilities
    in your training and prediction Lambda functions.
"""
# TODO - fix model utils paths in lambda functions
import pandas as pd
import numpy as np
import yfinance as yf

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

def create_sequences(train_data, target_data, seq_length):
    X = []
    y = []
    for i in range(len(train_data) - seq_length):
        X.append(train_data[i:i+seq_length])
        y.append(target_data[i+seq_length])
    return np.array(X), np.array(y)

def create_sequences_multi(training_data, target_data, seq_length, output_steps):
    X = []
    y = []
    for i in range(0, len(training_data) - seq_length - output_steps + 1, output_steps):
        X.append(training_data[i:i+seq_length])
        y.append(target_data[i+seq_length:i+seq_length+output_steps, 0]) 
    return np.array(X), np.array(y)

def load_past_data(per="1y"):
    # load ftse data from past 30 days
    yfinance_df = yf.download("^FTSE", period=per)

    yfinance_df.reset_index(inplace=True)            
    yfinance_df.set_index("Date", inplace=True)   

    yfinance_df.index = pd.to_datetime(yfinance_df.index)

    yfinance_df['Future Close'] = yfinance_df['Close'].shift(-1)
    yfinance_df['Close-5'] = yfinance_df['Close'].shift(5)

    yfinance_df.drop(inplace=True, index=yfinance_df.index[-1]) #Drop last row as it has no future close
    yfinance_df.drop(inplace=True, index=yfinance_df.index[0:5]) #Drop first 5 rows as it has no t-5

    yfinance_df = yfinance_df[['Open', 'High', 'Low', 'Close', 'Close-5', 'Future Close']]
    
    yfinance_df.columns = yfinance_df.columns.droplevel(1)  
    yfinance_df.index = yfinance_df.index.tz_localize(None)

    return yfinance_df






