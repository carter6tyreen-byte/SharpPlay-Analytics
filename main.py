import sys
import os
import logging
import json

# Force the directory into the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from api_client import fetch_sports_data, fetch_market_odds
from processor import process_raw_api_data
from prediction_engine import run_hr_prediction_model
from optimizer import get_optimal_bets

def save_data(data, filename='final_data.json'):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info(f"Successfully saved results to {filename}")
    except Exception as e:
        logging.error(f"Failed to save data: {e}")
        raise

def main():
    logging.info("--- Pipeline Started ---")
    
    # Retrieve the API key from the environment
    api_key = os.getenv('RAPIDAPI_KEY')
    if not api_key:
        logging.error("RAPIDAPI_KEY not found. Please set the environment variable.")
        return

    # 1. Pipeline Logic
    raw_data = fetch_sports_data(api_key=api_key)
    market_odds = fetch_market_odds(api_key=api_key)
    
    clean_df = process_raw_api_data(raw_data)
    
    if not clean_df.empty:
        predictions = run_hr_prediction_model(clean_df)
        optimal_bets = get_optimal_bets(predictions, market_odds)
        
        # 2. Save Results
        save_data(optimal_bets)
    else:
        logging.warning("No data processed. Pipeline ending.")

    logging.info("--- Execution Complete ---")

if __name__ == "__main__":
    main()
