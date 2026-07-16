import requests, json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / 'data' / 'today_matchups.json'

def fetch_today_matchups():
    url = "https://statsapi.mlb.com/api/v1/schedule"
    today = datetime.now().strftime('%Y-%m-%d')
    params = {"sportId": 1, "startDate": today, "endDate": today}
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    
    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(response.json(), f, indent=4)
    print(f"Saved to {OUTPUT_FILE}")
