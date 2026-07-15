import requests
import os
from datetime import datetime, timedelta

def fetch_mlb_api():
    # Targets tomorrow (July 16)
    target_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    # Use standard 'schedule' endpoint
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={target_date}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("dates") and data["dates"][0].get("games"):
                return data, "MLB"
    except Exception as e:
        print(f"MLB API Error: {e}")
    return None, None

def fetch_espn_data():
    # Use ESPN's public scoreboard API as a reliable fallback
    target_date = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")
    url = f"https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates={target_date}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("events"):
                return data, "ESPN"
    except Exception as e:
        print(f"ESPN API Error: {e}")
    return None, None

def update_html(data, source):
    matchup, status = "N/A", "N/A"
    try:
        if source == "MLB":
            game = data["dates"][0]["games"][0]
            away = game["teams"]["away"]["team"]["name"]
            home = game["teams"]["home"]["team"]["name"]
            matchup = f"{away} @ {home}"
            status = game["status"]["detailedState"]
        elif source == "ESPN":
            event = data["events"][0]
            matchup = event["name"]
            status = event["status"]["type"]["description"]
    except Exception:
        return

    # Write the file
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
    html = f"<html><body><h1>Latest MLB Stats ({source})</h1><p>{matchup} - {status}</p></body></html>"
    with open(output_path, "w") as f:
        f.write(html)

if __name__ == "__main__":
    # Logic: Try MLB first, if that fails, try ESPN
    data, source = fetch_mlb_api()
    if not data:
        data, source = fetch_espn_data()
        
    if data:
        update_html(data, source)
    else:
        print("No game data found from either source. Keeping current file.")
