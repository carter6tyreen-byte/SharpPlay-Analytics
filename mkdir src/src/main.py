from matchup_scraper import fetch_today_matchups
from data_processor import process_matchup_data 

def run_pipeline():
    print("Starting SharpPLAY Analytics pipeline...")
    fetch_today_matchups()
    process_matchup_data()
    print("Pipeline complete.")

if __name__ == "__main__":
    run_pipeline()
