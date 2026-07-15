import requests
import os
from datetime import datetime, timedelta

def get_games_for_date(date_str):
    # 1. Try Official MLB API
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date_str}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("dates") and data["dates"][0].get("games"):
                return data["dates"][0]["games"], "MLB"
    except Exception: pass
    
    # 2. Fallback to ESPN API
    espn_date = date_str.replace("-", "")
    url = f"https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates={espn_date}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("events"):
                return data["events"], "ESPN"
    except Exception: pass
    
    return [], None

def update_html():
    table_rows = []
    # Check the next 7 days
    for i in range(7):
        target_date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        games, source = get_games_for_date(target_date)
        
        for game in games:
            if source == "MLB":
                away = game["teams"]["away"]["team"]["name"]
                home = game["teams"]["home"]["team"]["name"]
                table_rows.append(f"<tr><td>{target_date}</td><td>{away} @ {home}</td></tr>")
            elif source == "ESPN":
                table_rows.append(f"<tr><td>{target_date}</td><td>{game['name']}</td></tr>")

    # Only update if we found games
    if not table_rows:
        print("No games found for the next 7 days. Keeping existing index.html.")
        return

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
    html = f"""<html><body><h1>MLB Schedule</h1><table border="1"><tr><th>Date</th><th>Matchup</th></tr>{''.join(table_rows)}</table><p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p></body></html>"""
    
    with open(output_path, "w") as f:
        f.write(html)
    print("Successfully updated index.html.")

if __name__ == "__main__":
    update_html()
