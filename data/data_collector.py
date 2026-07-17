import requests
import json
import os

def fetch_daily_schedule():
    url = "https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&date=2026-07-17"
    response = requests.get(url)
    
    if response.status_code == 200:
        # Save to the data folder
        with open('data/today_matchups.json', 'w') as f:
            json.dump(response.json(), f)
            print("Successfully updated full schedule in data folder.")
    else:
        print(f"Failed to fetch data: {response.status_code}")

if __name__ == "__main__":
    fetch_daily_schedule()
