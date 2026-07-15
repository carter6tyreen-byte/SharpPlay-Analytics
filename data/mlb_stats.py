import requests
import os
from datetime import datetime, timedelta

def fetch_mlb_data():
    # Targets tomorrow (July 16) to see if we can catch the first second-half games
    target_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    # Use the general 'schedule' endpoint, not 'schedule/live'
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={target_date}"
    
    print(f"DEBUG: Fetching URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("dates") and data["dates"][0].get("games"):
            return data, "MLB"
    except Exception as e:
        print(f"MLB API Error: {e}")

    # Fallback to ESPN if MLB is empty
    print("MLB API empty, trying ESPN...")
    espn_date = target_date.replace("-", "")
    espn_url = f"https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates={espn_date}"
    try:
        response = requests.get(espn_url, timeout=10)
        data = response.json()
        if data.get("events"):
            return data, "ESPN"
    except Exception as e:
        print(f"ESPN API Error: {e}")
        
    return None, None

def update_html(data, source):
    # Standardize parsing based on source
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
        pass

    # Write HTML...
    # (Use your existing writing logic here)
