import sys
import os
import logging
import json

# Force the current directory into the system path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Import modules with absolute certainty of path resolution
from api_client import fetch_sports_data, fetch_market_odds
from processor import process_raw_api_data, filter_starworld_criteria
from prediction_engine import run_hr_prediction_model
from starworld_optimizer import get_optimal_bets_with_sizing

def main():
    logging.info("--- Pipeline Started ---")
    
    api_key = os.getenv('RAPIDAPI_KEY')
    if not api_key:
        logging.error("RAPIDAPI_KEY not found. Pipeline aborting.")
        return

    # 1. Pipeline Execution
    raw_data = fetch_sports_data(api_key=api_key)
    market_odds = fetch_market_odds(api_key=api_key)
    
    clean_df = process_raw_api_data(raw_data)
    validated_df = filter_starworld_criteria(clean_df)
    
    if not validated_df.empty:
        predictions = run_hr_prediction_model(validated_df)
        optimal_bets = get_optimal_bets_with_sizing(predictions, market_odds)
        
        # 2. Output
        try:
            with open('final_data.json', 'w') as f:
                json.dump(optimal_bets.to_dict(orient='records'), f, indent=4)
            logging.info("Results saved successfully.")
        except Exception as e:
            logging.error(f"Failed to save: {e}")
    else:
        logging.warning("No data met Starworld criteria. Pipeline ending.")

    logging.info("--- Execution Complete ---")

if __name__ == "__main__":
    main()
