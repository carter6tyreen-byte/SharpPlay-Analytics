import requests
import json

def load_matchup_data():
    """Fetches all MLB games for today, including live and finished games."""
    # sportId=1 is MLB. Including specific statuses to capture everything.
    url = "https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.json()
        else:
            return {"dates": []}
    except Exception as e:
        print(f"Error fetching data: {e}")
        return {"dates": []}
