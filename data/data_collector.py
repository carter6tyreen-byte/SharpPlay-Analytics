import requests
import json
import os
from datetime import datetime

def fetch_and_save_matchups():
    today = datetime.now().strftime('%Y-%m-%d')
    # Added probablePitcher to hydration so your app can see them
    url = f"https://statsapi.mlb.com/api/v1/schedule?hydrate=lineups,pitchers,probablePitcher(note)&date={today}&sportId=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        os.makedirs('data', exist_ok=True)
        with open('data/today_matchups.json', 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Successfully saved full slate for {today}.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_save_matchups()
