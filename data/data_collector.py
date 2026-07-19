import requests
import json
import os
from datetime import datetime

def fetch_and_save_matchups():
    # 1. Use the current date (2026-07-19)
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 2. Correct URL for the full league schedule
    # Note: Removed team-specific filters to ensure ALL games are returned
    url = f"https://statsapi.mlb.com/api/v1/schedule?hydrate=lineups,pitchers&date={today}&sportId=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # 3. Ensure the 'data' directory exists
        os.makedirs('data', exist_ok=True)
        
        # 4. Save to the file that app.py reads
        with open('data/today_matchups.json', 'w') as f:
            json.dump(data, f, indent=4)
            
        print(f"Successfully saved {len(data.get('dates', [{}])[0].get('games', []))} games for {today}.")
        
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    fetch_and_save_matchups()
