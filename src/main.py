import logging
import sys
from matchup_scraper import fetch_today_matchups
from data_processor import process_raw_data
from db_manager import store_pre_game_snapshot
from models import PreGameSnapshot

# Configure logging to see the pipeline progress in GitHub Actions
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline():
    """
    Orchestrates the SharpPLAY Analytics pipeline in defined phases.
    """
    logging.info("Starting SharpPLAY Pipeline...")

    try:
        # Phase 1: Extraction
        logging.info("Phase 1: Extracting matchup data...")
        raw_data = fetch_today_matchups()
        
        # Phase 2: Transformation
        logging.info("Phase 2: Processing features...")
        processed_data = process_raw_data(raw_data)
        
        # Phase 3: Loading
        logging.info("Phase 3: Saving to historical database...")
        for game_id, features in processed_data.items():
            # Creating the model instance we defined
            snapshot = PreGameSnapshot(
                game_id=game_id,
                date="2026-07-16", # Example date; should be dynamic
                player=features.get("player"),
                features=features
            )
            store_pre_game_snapshot(snapshot)
            
        logging.info("Pipeline completed successfully.")

    except Exception as e:
        logging.error(f"Pipeline failed during execution: {e}")
        # Exit with error code so GitHub Actions marks the run as failed
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
