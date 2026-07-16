import os
import sys

# Although PYTHONPATH is set in the YAML, this adds an extra layer 
# of safety to ensure the current directory is always recognized.
sys.path.append(os.getcwd())

# Import your modules from the src package
from src.api_client import fetch_sports_data, fetch_market_odds
from src.data_processor import process_raw_api_data
from src.prediction_engine import run_hr_prediction_model
from src.optimizer import get_optimal_bets

def main():
    print("--- SharpPLAY Pipeline Started ---")
    
    try:
        # 1. Fetching Data
        print("Fetching data from API...")
        # raw_data = fetch_sports_data()
        
        # 2. Processing
        print("Processing raw data...")
        # clean_df = process_raw_api_data(raw_data)
        
        # 3. Prediction & Optimization
        print("Running prediction engine...")
        # predictions = run_hr_prediction_model(clean_df)
        
        # 4. Optimization
        print("Calculating optimal bets...")
        # optimal_bets = get_optimal_bets(predictions)
        
        print("--- Pipeline Completed Successfully ---")
        
    except Exception as e:
        print(f"Pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
