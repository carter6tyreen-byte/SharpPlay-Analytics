import requests
import os
from datetime import datetime, timedelta

def fetch_mlb_api():
    # Targets tomorrow to bypass the All-Star break empty data
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={tomorrow}"
    print(f"DEBUG: Trying MLB API: {url}")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("dates") and data["dates"][0].get("games"):
                return data
    except Exception as e:
        print(f"MLB API Error: {e}")
    return None

def fetch_espn_data():
    tomorrow_fmt = (datetime.now() + timedelta(days=1)).strftime("%Y%m%d")
    url = f"https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates={tomorrow_fmt}"
    print(f"DEBUG: Trying ESPN API: {url}")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("events"):
                return data
    except Exception as e:
        print(f"ESPN API Error: {e}")
    return None

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
    except (KeyError, IndexError):
        return

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
    html = f"""<html><body><h1>Latest MLB Stats ({source})</h1>
    <table border="1"><tr><th>Matchup</th><th>Result</th></tr>
    <tr><td>{matchup}</td><td>{status}</td></tr></table>
    <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p></body></html>"""
    
    with open(output_path, "w") as f:
        f.write(html)
    print(f"Successfully updated with {source} data.")

if __name__ == "__main__":
    # Attempt Primary MLB API
    data = fetch_mlb_api()
    if data:
        update_html(data, "MLB")
    else:
        # Fallback to ESPN API
        print("MLB data missing, trying ESPN...")
        data = fetch_espn_data()
        if data:
            update_html(data, "ESPN")
        else:
            print("Both sources returned no data. Keeping existing index.html.")
