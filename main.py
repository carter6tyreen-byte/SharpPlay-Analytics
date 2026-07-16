import sys
import os

# Dynamically adds the directory containing main.py to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api_client import fetch_sports_data, fetch_market_odds
from data_processor import process_raw_api_data
# ... rest of your imports
import sys
import os
import logging

# Path Management
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from api_client import fetch_sports_data, fetch_market_odds
from data_processor import process_raw_api_data
from prediction_engine import run_hr_prediction_model
from optimizer import get_optimal_bets

def main():
    logging.info("--- Pipeline Started ---")

    # 1. Fetch
    raw_data = fetch_sports_data()
    market_odds = fetch_market_odds()
    
    # 2. Process
    clean_df = process_raw_api_data(raw_data)
    
    # 3. Predict (The Connection)
    if not clean_df.empty:
        logging.info("Running prediction engine...")
        predictions = run_hr_prediction_model(clean_df)
        
        # 4. Optimize
        optimal_bets = get_optimal_bets(predictions, market_odds)
        logging.info(f"Generated {len(optimal_bets)} optimal bets.")
    else:
        logging.error("Pipeline halted: Data cleaning failed.")

    logging.info("--- Execution Complete ---")

if __name__ == "__main__":
    main()
