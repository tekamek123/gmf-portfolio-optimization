import pandas as pd
import numpy as np
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import plotting
import matplotlib.pyplot as plt
from typing import Dict, Tuple

class PortfolioOptimizer:
    """Handles Modern Portfolio Theory (MPT) optimization using PyPortfolioOpt"""
    
    def __init__(self, price_data: pd.DataFrame):
        """
        Initialize with historical price data
        price_data: DataFrame with dates as index and tickers as columns
        """
        self.price_data = price_data
        self.mu = None
        self.S = None

    def calculate_metrics(self):
        """Calculate expected returns and sample covariance matrix"""
        # Calculate annualised mean daily returns
        self.mu = expected_returns.mean_historical_return(self.price_data)
        # Calculate annualised sample covariance matrix
        self.S = risk_models.sample_cov(self.price_data)
        return self.mu, self.S

    def optimize_performance(self, target_return: float = None) -> Dict[str, float]:
        """
        Find the weights that maximize the Sharpe ratio or achieve a target return
        """
        if self.mu is None or self.S is None:
            self.calculate_metrics()
            
        ef = EfficientFrontier(self.mu, self.S)
        
        if target_return:
            weights = ef.efficient_return(target_return)
        else:
            # Maximize Sharpe ratio
            weights = ef.max_sharpe()
            
        cleaned_weights = ef.clean_weights()
        return dict(cleaned_weights)

    def get_performance(self, weights: Dict[str, float]) -> Tuple[float, float, float]:
        """
        Calculate expected annual return, volatility and Sharpe ratio for given weights
        """
        ef = EfficientFrontier(self.mu, self.S)
        ef.set_weights(weights)
        return ef.portfolio_performance(verbose=False)

    def plot_efficient_frontier(self):
        """Generate a plot of the Efficient Frontier"""
        if self.mu is None or self.S is None:
            self.calculate_metrics()
            
        fig, ax = plt.subplots(figsize=(10, 6))
        # This is a bit complex with pypfopt plotting, we'll do a simplified version
        # for the dashboard or just return the metrics for a plotly chart
        return fig
