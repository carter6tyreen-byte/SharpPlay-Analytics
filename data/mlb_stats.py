import requests
import os
from datetime import datetime, timedelta

def get_games_for_date(date_str):
    # Attempt MLB API first
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date_str}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("dates") and data["dates"][0].get("games"):
                return data["dates"][0]["games"], "MLB"
    except Exception:
        pass
    
    # Fallback to ESPN API
    espn_date = date_str.replace("-", "")
    url = f"https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard?dates={espn_date}"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("events"):
                return data["events"], "ESPN"
    except Exception:
        pass
    
    return [], None

def update_html():
    all_games = []
    # Loop for next 7 days
    for i in range(7):
        target_date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        games, source = get_games_for_date(target_date)
        for game in games:
            # Normalize data based on source
            if source == "MLB":
                away = game["teams"]["away"]["team"]["name"]
                home = game["teams"]["home"]["team"]["name"]
                all_games.append(f"<tr><td>{target_date}</td><td>{away} @ {home}</td></tr>")
            elif source == "ESPN":
                all_games.append(f"<tr><td>{target_date}</td><td>{game['name']}</td></tr>")

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
    html = f"""<html><body><h1>MLB Schedule (Next 7 Days)</h1>
    <table border="1"><tr><th>Date</th><th>Matchup</th></tr>
    {''.join(all_games) if all_games else '<tr><td colspan="2">No games found this week.</td></tr>'}
    </table>
    <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p></body></html>"""
    
    with open(output_path, "w") as f:
        f.write(html)

if __name__ == "__main__":
    update_html()
