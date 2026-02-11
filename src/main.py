from src.data_processing import DataIngestion, ProjectConfig
import sys
import os

def run_pipeline():
    """Main execution entry point for the project"""
    print("🚀 Week 12 Portfolio Transformation Pipeline Starting")
    print("-" * 50)
    
    # Initialize
    config = ProjectConfig()
    ingestion = DataIngestion(config)
    
    # Execute Ingestion
    raw_data = ingestion.fetch_data()
    if not raw_data:
        print("❌ Data ingestion failed. Exiting.")
        sys.exit(1)
        
    combined_data = ingestion.combine_and_save(raw_data)
    print(f"✅ Successfully processed {len(combined_data)} records.")
    print("-" * 50)
    print("🎯 Phase 1 (Ingestion) Complete.")

if __name__ == "__main__":
    # Adjust path to ensure local imports work during development
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    run_pipeline()
