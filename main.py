import sys
import os
import logging

# 1. Path Management (The "Golden Fix")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 2. Logging Configuration
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 3. Your Imports
from api_client import fetch_sports_data, fetch_market_odds
from data_processor import process_raw_api_data
from prediction_engine import run_hr_prediction_model
from optimizer import get_optimal_bets

def main():
    logging.info("--- Pipeline Started ---")
    
    # Example of how to use it:
    # logging.info("Fetching sports data...")
    
    logging.info("--- Execution Complete ---")

if __name__ == "__main__":
    main()
