import sys
import os

# Explicitly add the root directory to the Python path
sys.path.append(os.getcwd())

# Now your direct imports will be resolved correctly
from api_client import fetch_sports_data, fetch_market_odds
from data_processor import process_raw_api_data
from prediction_engine import run_hr_prediction_model
from optimizer import get_optimal_bets

def main():
    print("--- Pipeline Started Successfully ---")
    # Your logic here...
    print("--- Execution Complete ---")

if __name__ == "__main__":
    main()
