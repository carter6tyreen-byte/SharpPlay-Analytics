import sys
import logging
from matchup_scraper import fetch_today_matchups
from data_processor import process_matchup_data

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline():
    try:
        logging.info("Starting pipeline...")
        
        # 1. Fetch
        raw_data = fetch_today_matchups()
        logging.info("Extraction successful.")
        
        # 2. Process
        results = process_matchup_data(raw_data)
        logging.info(f"Processing complete. Results: {results}")
        
        return results
        
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
