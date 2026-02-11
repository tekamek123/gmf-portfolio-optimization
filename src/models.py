from typing import Tuple, Dict, Any, Optional
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import os

class TimeSeriesModel:
    """Base class for time series forecasting models"""
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.model = None

    def train(self, data: pd.Series):
        raise NotImplementedError

    def predict(self, steps: int) -> np.ndarray:
        raise NotImplementedError

class ARIMAModel(TimeSeriesModel):
    """ARIMA Model implementation for financial forecasting"""
    
    def train(self, data: pd.Series, order: Tuple[int, int, int] = (5, 1, 0)):
        """Train ARIMA model on the provided series"""
        print(f"📉 Training ARIMA for {self.ticker}...")
        self.model = ARIMA(data, order=order).fit()
        return self.model

    def predict(self, steps: int) -> np.ndarray:
        """Forecast future values"""
        if self.model is None:
            raise ValueError("Model must be trained before prediction.")
        return self.model.forecast(steps=steps)

class LSTMForecaster(TimeSeriesModel):
    """LSTM Deep Learning implementation for forecasting"""
    
    def __init__(self, ticker: str):
        super().__init__(ticker)
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def _prepare_sequences(self, data: np.ndarray, window: int = 60):
        """Build sequences for LSTM input"""
        X, y = [], []
        for i in range(window, len(data)):
            X.append(data[i-window:i, 0])
            y.append(data[i, 0])
        return np.array(X), np.array(y)

    def train(self, data: pd.Series, epochs: int = 10, batch_size: int = 32):
        """Train LSTM model on historical prices"""
        print(f"🧠 Training LSTM for {self.ticker}...")
        
        # Scale data
        scaled_data = self.scaler.fit_transform(data.values.reshape(-1, 1))
        X, y = self._prepare_sequences(scaled_data)
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))

        # Build Model
        model = Sequential([
            LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 1)),
            Dropout(0.2),
            LSTM(units=50, return_sequences=False),
            Dropout(0.2),
            Dense(units=25),
            Dense(units=1)
        ])
        
        model.compile(optimizer='adam', loss='mean_squared_error')
        model.fit(X, y, batch_size=batch_size, epochs=epochs, verbose=0)
        self.model = model
        return self.model

    def predict(self, last_sequence: np.ndarray, steps: int = 30) -> np.ndarray:
        """Forecast using sliding window approach"""
        if self.model is None:
            raise ValueError("Model must be trained before prediction.")
            
        current_seq = last_sequence.copy()
        predictions = []
        
        for _ in range(steps):
            pred = self.model.predict(current_seq.reshape(1, -1, 1), verbose=0)
            predictions.append(pred[0, 0])
            # Slide window
            current_seq = np.append(current_seq[1:], pred)
            
        return self.scaler.inverse_transform(np.array(predictions).reshape(-1, 1)).flatten()
