import pytest
import pandas as pd
import os
from src.data_processing import DataIngestion, ProjectConfig

@pytest.fixture
def mock_config(tmp_path):
    """Create a temporary config for testing"""
    processed_path = tmp_path / "processed" / "test_data.csv"
    return ProjectConfig(
        TICKERS=['SPY'],
        START_DATE="2024-01-01",
        END_DATE="2024-01-10",
        PROCESSED_DATA_PATH=str(processed_path)
    )

def test_data_ingestion_fetch(mock_config):
    """Test that data can be fetched (integrates with yfinance)"""
    ingestion = DataIngestion(mock_config)
    data = ingestion.fetch_data()
    
    assert 'SPY' in data
    assert isinstance(data['SPY'], pd.DataFrame)
    assert not data['SPY'].empty

def test_data_combination_and_saving(mock_config):
    """Test that data is combined and saved correctly"""
    ingestion = DataIngestion(mock_config)
    
    # Create manual data to avoid network dependance in this logic test
    test_df = pd.DataFrame({'Close': [100, 101, 102]}, 
                          index=pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-03']))
    data_dict = {'SPY': test_df}
    
    combined = ingestion.combine_and_save(data_dict)
    
    assert combined.shape == (3, 1)
    assert 'SPY' in combined.columns
    assert os.path.exists(mock_config.PROCESSED_DATA_PATH)
    
    # Verify file content
    saved_df = pd.read_csv(mock_config.PROCESSED_DATA_PATH, index_col=0)
    assert len(saved_df) == 3
