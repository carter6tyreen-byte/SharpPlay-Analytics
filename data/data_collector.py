import requests
import json
import os
from datetime import datetime, timedelta

os.makedirs('data', exist_ok=True)

def fetch_and_save_matchups():
    today = datetime.now().strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    url = f"https://statsapi.mlb.com/api/v1/schedule?hydrate=lineups,pitchers&startDate={today}&endDate={tomorrow}&sportId=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open('data/today_matchups.json', 'w') as f:
            json.dump(response.json(), f, indent=4)
        print(f"Successfully collected data for {today} and {tomorrow}.")
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    fetch_and_save_matchups()
