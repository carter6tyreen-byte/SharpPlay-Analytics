import requests
import pandas as pd

# Define the API URL for MLB data
API_URL = "https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1&startDate=2026-07-16&endDate=2026-07-16"

# Fetch data from the API
response = requests.get(API_URL)
data = response.json()

# Process games
if 'dates' in data and len(data['dates']) > 0:
    for game in data['dates'][0]['games']:
        away_name = game['teams']['away']['team']['name']
        home_name = game['teams']['home']['team']['name']
        
        # Construct game data structure
        game_data = {
            "matchup": f"{away_name} vs {home_name}",
            "teams": {
                "home": {"name": home_name},
                "away": {"name": away_name}
            }
        }
        print(f"Processed: {game_data['matchup']}")

# Save analytics data to JSON
# Ensure the directory exists and data is written correctly
