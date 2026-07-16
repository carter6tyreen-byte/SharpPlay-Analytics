from src.matchup_scraper import fetch_today_matchups
# Assuming you have your processing logic in data_processor.py
from src.data_processor import process_matchup_data 

def run_pipeline():
    print("Starting SharpPLAY Analytics pipeline...")
    
    # 1. Fetch the raw data
    print("Fetching today's matchups...")
    fetch_today_matchups()
    
    # 2. Process the data for the dashboard
    print("Processing metrics...")
    process_matchup_data()
    
    print("Pipeline complete. Data is ready for deployment.")

if __name__ == "__main__":
    run_pipeline()
