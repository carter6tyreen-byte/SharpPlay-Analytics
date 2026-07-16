# main.py
# Use absolute imports now that the root is in the PYTHONPATH
from api_client import fetch_sports_data, fetch_market_odds
from data_processor import process_raw_api_data
from prediction_engine import run_hr_prediction_model
from optimizer import get_optimal_bets

def main():
    print("--- SharpPLAY Pipeline Started ---")
    # Your logic here
    print("--- Execution Successful ---")

if __name__ == "__main__":
    main()
