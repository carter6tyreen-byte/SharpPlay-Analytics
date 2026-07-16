import sys
import logging

# Configure logging so you can see output in your GitHub Actions logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from matchup_scraper import fetch_today_matchups
from data_processor import process_matchup_data

def run_pipeline():
    """Orchestrates the analytics pipeline."""
    try:
        logging.info("Starting matchup data extraction...")
        # Assuming these return success/failure or paths to data
        fetch_today_matchups()
        
        logging.info("Data extraction complete. Starting processing...")
        process_matchup_data()
        
        logging.info("Pipeline completed successfully.")
        
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        # Exit with a non-zero code so the GitHub Action marks the step as failed
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
