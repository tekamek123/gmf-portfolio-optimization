import shap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Any, Tuple

class ModelExplainer:
    """Wrapper for SHAP explainability on LSTM models"""
    
    def __init__(self, model: Any, background_data: np.ndarray):
        """
        Initialize with a trained model and background samples
        background_data should be in form (samples, window, features)
        """
        self.model = model
        self.background_data = background_data
        self.explainer = shap.GradientExplainer(model, background_data)

    def explain(self, test_data: np.ndarray) -> np.ndarray:
        """Calculate SHAP values for test samples"""
        return self.explainer.shap_values(test_data)

    def plot_importance(self, shap_values: list, feature_names: list):
        """
        Generate a summary plot of feature importance
        Note: For LSTM, we aggregate across the time dimension
        """
        # SHAP values for GradientExplainer with LSTM can be [samples, window, features]
        # We handle both list and array outputs
        if isinstance(shap_values, list):
            vals = np.abs(shap_values[0])
        else:
            vals = np.abs(shap_values)
            
        # Aggregate importance across samples and time window
        # vals shape: (sequences, window, 1)
        importance = vals.mean(axis=(0, 1)).flatten()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        pd.Series(importance, index=feature_names).sort_values().plot(kind='barh', ax=ax)
        ax.set_title("Feature Importance (SHAP)")
        ax.set_xlabel("Mean Absolute SHAP Value")
        plt.tight_layout()
        return fig

    def plot_time_importance(self, shap_values: list, window: int):
        """Visualize which lags in the time window were most important"""
        if isinstance(shap_values, list):
            vals = np.abs(shap_values[0])
        else:
            vals = np.abs(shap_values)
            
        # vals shape: (sequences, window, 1) -> aggregate across sequences and features
        temporal_importance = vals.mean(axis=(0, 2)).flatten()
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(range(window), temporal_importance, marker='o', color='#2ca02c')
        ax.set_title("Temporal Importance (Impact of specific lags)")
        ax.set_xlabel("Lag (Days ago, 0=oldest, 60=most recent)")
        ax.set_ylabel("Mean Impact")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        return fig
