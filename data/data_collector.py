import requests
import json

def load_matchup_data():
    """Fetches and returns the latest MLB schedule data."""
    url = "https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return {} # Return empty dict on error to prevent crashes
