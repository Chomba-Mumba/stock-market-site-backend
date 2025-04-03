import pytest
import numpy as np
import pandas as pd
import tensorflow as tf
from random import random
from unittest.mock import patch, MagicMock
from sklearn.preprocessing import MinMaxScaler
from services.model_utils import load_past_data #TODO - adjust references for services in model tests in Pipelines and test files.
import os
from ..predictions_performance import predict_multiple_steps, scale_data, unscale_data, predict_next_week, predict_next_day

@pytest.fixture
def mock_train_data():
    mock_train_data = pd.DataFrame(columns=["Close-5","Close"], index=range(50))
    mock_train_data.iloc[:, :] = [[random(), random()] for _ in range(0,50)]
    mock_train_data["Close-5"] = mock_train_data["Close-5"].shift(-5)
    mock_train_data = mock_train_data[:-5]
    return mock_train_data

@pytest.fixture
def mock_scaler():
    return MinMaxScaler()

#TODO - Replace with MagicMock
class MockModel:
    def predict(self, input_data):
        return np.array([[0.9649677]], dtype=np.float32)
    
# TODO - modify creation of csv with every test, add decorator for predict_next_day

@patch("services.model_utils.load_past_data")
def test_scale_data(mock_load_past_data, mock_train_data):
    mock_load_past_data.return_value = mock_train_data
    scaled_data, scaler = scale_data(mock_train_data)
    assert scaled_data.shape == (45, 2)
    assert isinstance(scaler, MinMaxScaler)

# @patch('tensorflow.keras.models import load_model')
def test_predict_multiple_steps(mock_train_data):
    mock_model = MockModel()

    scaled_data, scaler = scale_data(mock_train_data)
    print(scaled_data)
    predictions = predict_multiple_steps(scaled_data, mock_model, scaler, seq_length=25, steps=5)
    
    assert len(predictions) == 5
    assert isinstance(scaler, MinMaxScaler)
    assert all(isinstance(p, float) for p in predictions)

def test_predict_next_week(mock_train_data, tmp_path):
    mock_model = MockModel()
    
    pred_path = tmp_path / "predictions.csv"
    pd.DataFrame({"Date": [], "Date + 1": [], "Date + 5": []}).to_csv(pred_path, index=False)
    
    pred_df = predict_next_week(pred_path, mock_model,train_df=mock_train_data)
    
    assert isinstance(pred_df, pd.DataFrame)
    assert len(pred_df) > 0

def test_predict_next_day(mock_train_data, tmp_path):

    mock_model = MockModel()
    data = [
            ["2024-02-01", 1.25, 1.45],
            ["2024-02-02", 1.30, 1.50],
            ["2024-02-03", None, 1.55], 
            ["2024-02-04", 1.40, 1.60],
            ["2024-02-05", 1.50, 1.65]
    ]   

    pred_path = tmp_path / "predictions.csv"
    pd.DataFrame(data, columns=["Date", "Date + 1", "Date + 5"]).to_csv(pred_path, index=False)
    
    pred_df = predict_next_day( pred_path, mock_train_data, mock_model)
    
    assert isinstance(pred_df, pd.DataFrame)
    assert len(pred_df) > 0

if __name__ == "__main__":
    import pytest
    import sys
    
    # Run pytest and exit with the appropriate status code
    sys.exit(pytest.main([__file__]))