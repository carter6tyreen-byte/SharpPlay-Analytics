import sys
from pathlib import Path

# Add the current directory to sys.path so it can find local files
sys.path.append(str(Path(__file__).parent))

from matchup_scraper import fetch_today_matchups
from data_processor import process_matchup_data 

def run_pipeline():
    print("Starting pipeline...")
    fetch_today_matchups()
    process_matchup_data()

if __name__ == "__main__":
    run_pipeline()
