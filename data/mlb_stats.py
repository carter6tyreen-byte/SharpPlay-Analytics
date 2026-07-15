import requests
import os
from datetime import datetime, timedelta

def get_games():
    all_games = []
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
                        all_games.append(f"<tr><td>{target_date}</td><td>{away} @ {home}</td></tr>")
        except Exception:
            continue 
            
    return all_games

def update_html():
    rows = get_games()
    
    # If no games are found for the entire week, show a friendly message instead of blank
    if not rows:
        table_content = "<tr><td colspan='2'>No upcoming games found this week.</td></tr>"
    else:
        table_content = "".join(rows)

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

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
    with open(output_path, "w") as f:
        f.write(html_content)
    print("Successfully updated index.html.")

if __name__ == "__main__":
    update_html()
