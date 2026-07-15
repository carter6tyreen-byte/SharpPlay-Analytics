import requests
import os
from datetime import datetime, timedelta

def get_games():
    all_games = []
    # Look at the next 7 days
    for i in range(7):
        target_date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={target_date}"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("dates"):
                    for game in data["dates"][0].get("games", []):
                        away = game["teams"]["away"]["team"]["name"]
                        home = game["teams"]["home"]["team"]["name"]
                        all_games.append(f"<tr><td>{target_date}</td><td>{away} @ {home}</td></tr>")
        except Exception:
            continue
    return all_games

def update_html():
    rows = get_games()
    # If no games found for the week, show a message instead of blank/N/A
    table_content = "".join(rows) if rows else "<tr><td colspan='2'>No games found this week.</td></tr>"

    html_content = f"""<html>
<body><h1>MLB Schedule (Next 7 Days)</h1>
<table border="1"><tr><th>Date</th><th>Matchup</th></tr>{table_content}</table>
<p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p></body></html>"""

    # Ensure we write to the correct root index.html
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
    with open(output_path, "w") as f:
        f.write(html_content)

if __name__ == "__main__":
    update_html()
