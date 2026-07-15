import requests
import os
from datetime import datetime, timedelta

def get_games():
    all_games = []
    # Loop through the next 7 days to ensure you capture games
    for i in range(7):
        target_date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={target_date}"
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # Check if games exist for this date
                if data.get("dates"):
                    for game in data["dates"][0].get("games", []):
                        away = game["teams"]["away"]["team"]["name"]
                        home = game["teams"]["home"]["team"]["name"]
                        all_games.append(f"<tr><td>{target_date}</td><td>{away} @ {home}</td></tr>")
        except Exception:
            continue # Skip days if the API call fails or is empty
            
    return all_games

def update_html():
    rows = get_games()
    
    # Safety: Do not overwrite index.html if no games are found for the whole week
    if not rows:
        print("No games found for the next week. Keeping existing index.html.")
        return

    html_content = f"""<html>
<head><title>MLB Schedule</title></head>
<body>
    <h1>MLB Schedule (Next 7 Days)</h1>
    <table border="1">
        <tr><th>Date</th><th>Matchup</th></tr>
        {"".join(rows)}
    </table>
    <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
</body>
</html>"""

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
    with open(output_path, "w") as f:
        f.write(html_content)
    print("Successfully updated index.html with the 7-day schedule.")

if __name__ == "__main__":
    update_html()
