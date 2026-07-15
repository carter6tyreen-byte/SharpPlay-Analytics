import requests
import os
from datetime import datetime, timedelta

def fetch_mlb_api():
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={tomorrow}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"MLB API Error: {e}")
    return None

def fetch_espn_data():
    tomorrow_fmt = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")
    url = f"https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates={tomorrow_fmt}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"ESPN API Error: {e}")
    return None

def update_html(data, source_name):
    if not data: return
    
    # Simple extraction logic (adjust based on which source succeeded)
    matchup, status = "Unknown", "Unknown"
    
    if source_name == "MLB":
        game = data.get("dates", [{}])[0].get("games", [{}])[0]
        away = game.get("teams", {}).get("away", {}).get("team", {}).get("name", "N/A")
        home = game.get("teams", {}).get("home", {}).get("team", {}).get("name", "N/A")
        matchup, status = f"{away} @ {home}", "Scheduled"
        
    elif source_name == "ESPN":
        event = data.get("events", [{}])[0]
        matchup = event.get("name", "N/A")
        status = event.get("status", {}).get("type", {}).get("description", "Scheduled")

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
    html_content = f"<html><body><h1>Latest MLB Stats ({source_name})</h1><table border='1'><tr><th>Matchup</th><th>Result</th></tr><tr><td>{matchup}</td><td>{status}</td></tr></table></body></html>"
    
    with open(output_path, "w") as f:
        f.write(html_content)

if __name__ == "__main__":
    # Try MLB first, fallback to ESPN
    data = fetch_mlb_api()
    if data and data.get("dates"):
        update_html(data, "MLB")
    else:
        print("MLB data empty, trying ESPN...")
        data = fetch_espn_data()
        if data and data.get("events"):
            update_html(data, "ESPN")
        else:
            print("Both sources failed.")
