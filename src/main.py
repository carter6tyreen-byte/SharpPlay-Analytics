import logging
import sys
from matchup_scraper import fetch_today_matchups
from data_processor import process_matchup_data
from models import PreGameSnapshot
from db_manager import store_pre_game_snapshot

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline():
    logging.info("Starting SharpPLAY Pipeline...")
    try:
        # Phase 1: Extraction
        logging.info("Phase 1: Fetching matchups...")
        raw_data = fetch_today_matchups()
        
        # Phase 2: Transformation
        logging.info("Phase 2: Processing features...")
        processed_data = process_matchup_data(raw_data)
        
        # Phase 3: Loading
        logging.info("Phase 3: Storing snapshots...")
        for game_id, features in processed_data.items():
            snapshot = PreGameSnapshot(
                game_id=game_id,
                date="2026-07-16",
                player=features.get("player"),
                features=features
            )
            store_pre_game_snapshot(snapshot)
            
        logging.info("Pipeline completed successfully.")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
