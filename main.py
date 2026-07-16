import sys
import os
import logging
import json

# Ensure the script can find its sibling files
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Import your modules
from api_client import fetch_sports_data, fetch_market_odds
from processor import process_raw_api_data, filter_starworld_criteria
from prediction_engine import run_hr_prediction_model
from Starworld_optimizer import get_optimal_bets_with_sizing

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
    
    # Retrieve environment variables
    api_key = os.getenv('RAPIDAPI_KEY')
    if not api_key:
        logging.error("RAPIDAPI_KEY not found. Pipeline aborting.")
        return

    # 1. Pipeline Execution
    raw_data = fetch_sports_data(api_key=api_key)
    market_odds = fetch_market_odds(api_key=api_key)
    
    # Clean data and apply Starworld validation filters
    clean_df = process_raw_api_data(raw_data)
    validated_df = filter_starworld_criteria(clean_df)
    
    if not validated_df.empty:
        # Run predictions
        predictions = run_hr_prediction_model(validated_df)
        
        # Optimize bets and apply Kelly Sizing
        optimal_bets = get_optimal_bets_with_sizing(predictions, market_odds)
        
        # 2. Save Results
        save_data(optimal_bets.to_dict(orient='records'))
    else:
        logging.warning("No data met Starworld criteria. Pipeline ending.")

    logging.info("--- Execution Complete ---")

if __name__ == "__main__":
    main()
