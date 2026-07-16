from matchup_scraper import fetch_today_matchups
from data_processor import process_matchup_data

if __name__ == "__main__":
    fetch_today_matchups()
    process_matchup_data()
