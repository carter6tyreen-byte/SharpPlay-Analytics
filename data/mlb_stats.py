import requests

def fetch_roster_data(game_id):
    """Fetches roster info for a specific game ID."""
    url = f"https://statsapi.mlb.com/api/v1/game/{game_id}/feed/live"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json().get("gameData", {})
        return {}
    except Exception as e:
        print(f"Error in fetch_roster_data: {e}")
        return {}
