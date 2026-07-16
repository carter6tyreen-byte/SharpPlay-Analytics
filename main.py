import sys
import os

# ADD THIS IMMEDIATELY: Force Python to look in the current working directory
sys.path.append(os.getcwd())

# NOW perform the imports
from src.api_client import fetch_sports_data, fetch_market_odds
from src.data_processor import process_raw_api_data
from src.prediction_engine import run_hr_prediction_model
from src.optimizer import get_optimal_bets

def main():
    print("Pipeline initialized successfully.")
    # Add your logic here
    print("Execution complete.")

if __name__ == "__main__":
    main()
