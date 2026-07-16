import sys
import os

# 1. Ensure the root directory is in the path so 'src' is found
sys.path.append(os.getcwd())

# 2. Imports from your src/ folder
from src.api_client import fetch_sports_data, fetch_market_odds
from src.data_processor import process_raw_api_data
from src.prediction_engine import run_hr_prediction_model
from src.optimizer import get_optimal_bets

def main():
    print("Starting SharpPLAY Pipeline...")
    
    # Example flow:
    # raw_data = fetch_sports_data()
    # clean_data = process_raw_api_data(raw_data)
    # predictions = run_hr_prediction_model(clean_data)
    # optimal_bets = get_optimal_bets(predictions)
    
    # print("Pipeline execution complete.")
    print("Imports successful! Pipeline is ready for data logic.")

if __name__ == "__main__":
    main()
