import requests
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def fetch_roster_data(game_id):
    """Fetches roster and game info for a specific MLB game ID using the official live feed API."""
    url = f"https://statsapi.mlb.com/api/v1/game/{game_id}/feed/live"
    headers = {
        "User-Agent": "SharpPlayAnalytics/1.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("gameData", {})
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching roster data for game {game_id}: {e}")
        return {}

if __name__ == "__main__":
    # Example active 2026 MLB game ID or fallback test ID
    sample_game_id = 775000 
    logging.info(f"Fetching live feed data for game ID: {sample_game_id}")
    
    roster_data = fetch_roster_data(sample_game_id)
    
    output_path = "analytics_data.json"
    with open(output_path, "w") as f:
        json.dump(roster_data, f, indent=4)
        
    logging.info(f"Successfully processed and saved game feed data to {output_path}")
