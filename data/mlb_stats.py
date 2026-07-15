import requests
import os
from datetime import datetime, timedelta

def get_games_for_week():
    all_rows = []
    # Loop through the next 7 days
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
                        all_rows.append(f"<tr><td>{target_date}</td><td>{away} @ {home}</td></tr>")
        except Exception:
            continue
    return all_rows

def update_html():
    rows = get_games_for_week()
    
    # If no games are found for the whole week, show a helpful message
    table_content = "".join(rows) if rows else "<tr><td colspan='2'>No games found this week.</td></tr>"

    html_content = f"""<html>
<head><title>MLB Schedule</title></head>
<body>
    <h1>MLB Schedule (Next 7 Days)</h1>
    <table border="1">
        <tr><th>Date</th><th>Matchup</th></tr>
        {table_content}
    </table>
    <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
</body>
</html>"""

    with open("index.html", "w") as f:
        f.write(html_content)

if __name__ == "__main__":
    update_html()
