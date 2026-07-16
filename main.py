import sys
import os
import logging
import json

# The "Golden Fix" for pathing
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api_client import fetch_sports_data, fetch_market_odds
from data_processor import process_raw_api_data
from prediction_engine import run_hr_prediction_model
from optimizer import get_optimal_bets

def main():
    logging.info("--- Pipeline Started ---")

    # 1. Pipeline Logic
    raw_data = fetch_sports_data()
    market_odds = fetch_market_odds()
    clean_df = process_raw_api_data(raw_data)
    
    if not clean_df.empty:
        predictions = run_hr_prediction_model(clean_df)
        optimal_bets = get_optimal_bets(predictions, market_odds)
        
        # 2. Save for the Dashboard
        # This converts your results into a format a website can read
        with open('final_data.json', 'w') as f:
            json.dump(optimal_bets, f)
        logging.info("Saved data to final_data.json")

    logging.info("--- Execution Complete ---")

if __name__ == "__main__":
    main()

import json
import logging

def save_data(data, filename='final_data.json'):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info(f"Successfully saved results to {filename}")
    except Exception as e:
        logging.error(f"Failed to save data: {e}")

# In your main() function:
# ... after optimal_bets = get_optimal_bets(...)
save_data(optimal_bets)

