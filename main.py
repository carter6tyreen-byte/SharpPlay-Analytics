# main.py
# Import directly from the files now in your root directory
from api_client import fetch_sports_data, fetch_market_odds
from data_processor import process_raw_api_data
from prediction_engine import run_hr_prediction_model
from optimizer import get_optimal_bets

def main():
    print("--- Pipeline Started (Flattened Structure) ---")
    
    # Your logic here
    # Example:
    # raw_data = fetch_sports_data(os.getenv("RAPIDAPI_KEY"))
    
    print("--- Execution Successful ---")

if __name__ == "__main__":
    main()
