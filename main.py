# main.py

# Remove the 'src.' prefix from all imports
from api_client import fetch_sports_data, fetch_market_odds
from data_processor import process_raw_api_data
from prediction_engine import run_hr_prediction_model
from optimizer import get_optimal_bets

def main():
    print("--- Pipeline Started ---")
    # Your logic here...
    print("--- Pipeline Execution Complete ---")

if __name__ == "__main__":
    main()
