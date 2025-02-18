from io import StringIO
import tensorflow as tf
import pandas as pd
import numpy as np
import datetime
import logging

import boto3

import pytest
from moto import mock_aws

from ftse_predictions_lambda.ftse_predictions import lambda_handler, get_csv_from_s3

@mock_aws
def test_lambda_handler_success():
    s3 = boto3.client('s3', region_name='eu-west-1')
    bucket_name = "test-bucket"
    file_key = "test.csv"

    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
    csv_content = "col1,col2\nval1,val2"
    s3.put_object(Bucket=bucket_name, Key=file_key, Body=csv_content)

    expected_rows = [['col1', 'col2'], ['val1', 'val2']]

    response = lambda_handler({'bucket_name': bucket_name, 'file_key': file_key}, {})
    assert response['body']  == expected_rows

@mock_aws
def test_lambda_handler_failure():
    s3 = boto3.client('s3', region_name='eu-west-1')
    bucket_name = "test-bucket"
    file_key = "example"

    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
    csv_content = ""
    s3.put_object(Bucket=bucket_name, Key=file_key, Body=csv_content)

    response = lambda_handler({'bucket_name': bucket_name}, {})
    assert response['statusCode']  == 400