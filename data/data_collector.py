import requests
import json
import os
from datetime import datetime

# Path to the file that your Streamlit app reads
DATA_FILE = 'data/today_matchups.json'

def fetch_and_save_matchups():
    # 1. Get today's date dynamically (2026-07-19)
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 2. API call for the full league schedule
    # sportId=1 ensures we get MLB games
    # No team filter is used so we get all matchups
    url = f"https://statsapi.mlb.com/api/v1/schedule?hydrate=lineups,pitchers&date={today}&sportId=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # 3. Ensure the 'data' directory exists
        if not os.path.exists('data'):
            os.makedirs('data')
            
        # 4. Overwrite with the fresh data
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
            
        print(f"Success: Updated {DATA_FILE} with data for {today}.")
        
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    fetch_and_save_matchups()
