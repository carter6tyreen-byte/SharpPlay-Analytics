import requests
import json
import os

# Ensure the data directory exists
os.makedirs('data', exist_ok=True)

def fetch_and_save_matchups():
    # Adding 'hydrate=lineups,pitchers' to get detailed player information
    url = "https://statsapi.mlb.com/api/v1/schedule?hydrate=lineups,pitchers&date=2026-07-19&sportId=1"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Save the full response with hydrated player data
        with open('data/today_matchups.json', 'w') as f:
            json.dump(data, f, indent=4)
        print("Data collected successfully with player details.")
        
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    fetch_and_save_matchups()
