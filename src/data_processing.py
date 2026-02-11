from dataclasses import dataclass, field
from typing import List, Dict, Optional
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import os

@dataclass(frozen=True)
class ProjectConfig:
    """Configuration for the portfolio management project"""
    TICKERS: List[str] = field(default_factory=lambda: ['TSLA', 'BND', 'SPY'])
    START_DATE: str = "2015-01-01"
    END_DATE: str = "2026-01-15"
    RAW_DATA_PATH: str = "data/raw/stock_data.csv"
    PROCESSED_DATA_PATH: str = "data/processed/portfolio_data.csv"

class DataIngestion:
    """Handles fetching and basic cleaning of financial data"""
    
    def __init__(self, config: ProjectConfig = ProjectConfig()):
        self.config = config

    def fetch_data(self) -> Dict[str, pd.DataFrame]:
        """
        Download historical financial data for configured tickers
        """
        data_dict = {}
        print(f"📊 Downloading data for: {self.config.TICKERS}")
        
        for ticker in self.config.TICKERS:
            try:
                df = yf.download(ticker, start=self.config.START_DATE, end=self.config.END_DATE)
                if df.empty:
                    print(f"⚠️  No data for {ticker}")
                    continue
                
                # Handling multi-index columns from recent yfinance versions
                if isinstance(df.columns, pd.MultiIndex):
                    df.columns = df.columns.droplevel(1)
                
                data_dict[ticker] = df
                print(f"✅ Downloaded {len(df)} rows for {ticker}")
            except Exception as e:
                print(f"❌ Error downloading {ticker}: {e}")
                
        return data_dict

    def combine_and_save(self, data_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        Combine multiple ticker dataframes into one and save to disk
        """
        combined = pd.DataFrame()
        
        for ticker, df in data_dict.items():
            # Use Adj Close if available, otherwise Close
            price_col = 'Adj Close' if 'Adj Close' in df.columns else 'Close'
            ticker_prices = df[[price_col]].rename(columns={price_col: ticker})
            
            if combined.empty:
                combined = ticker_prices
            else:
                combined = combined.join(ticker_prices, how='outer')
        
        # Clean data
        combined = combined.dropna()
        
        # Save
        os.makedirs(os.path.dirname(self.config.PROCESSED_DATA_PATH), exist_ok=True)
        combined.to_csv(self.config.PROCESSED_DATA_PATH)
        print(f"💾 Processed data saved to {self.config.PROCESSED_DATA_PATH}")
        
        return combined

if __name__ == "__main__":
    # Quick test run
    ingestion = DataIngestion()
    raw_data = ingestion.fetch_data()
    processed_df = ingestion.combine_and_save(raw_data)
    print(f"📊 Final combined shape: {processed_df.shape}")
