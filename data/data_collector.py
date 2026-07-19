import requests
import json
import os
from datetime import datetime, timedelta

os.makedirs('data', exist_ok=True)

def fetch_and_save_matchups():
    # Dynamically generate dates
    today = datetime.now().strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Use startDate/endDate for a range instead of just one date
    url = f"https://statsapi.mlb.com/api/v1/schedule?hydrate=lineups,pitchers&startDate={today}&endDate={tomorrow}&sportId=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open('data/today_matchups.json', 'w') as f:
            json.dump(response.json(), f, indent=4)
        print(f"Data collected for {today} and {tomorrow}.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_save_matchups()
