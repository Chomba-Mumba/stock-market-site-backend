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

def un_yfinance_update(df1):
    df1 = df1.reset_index()
    t = df1.keys()[1][1] # ticker
    d = {
        "Datetime":df1[('Datetime','')],
        "Open":df1[('Open',t)],
        "High":df1[('High',t)],
        "Low":df1[('Low',t)],
        "Close":df1[('Close',t)],
         }
    
    df2 = pd.DataFrame(d)

    return df2

def load_past_data(per="1y"):
    # load ftse data from past 30 days
    yfinance_df = yf.download("^FTSE", period=per)
    #yfinance_df = un_yfinance_update(yfinance_df_temp)

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
load_past_data()