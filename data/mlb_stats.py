import requests
import os
from datetime import datetime, timedelta

def fetch_mlb_data():
    # Fetching tomorrow's date to account for the current All-Star break
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    url = f"https://statsapi.mlb.com/api/v1/schedule/live?sportId=1&date={tomorrow}"
    
    print(f"DEBUG: Fetching schedule for: {tomorrow}")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
    return None

def update_html(data):
    if not data or "dates" not in data or not data["dates"]:
        print("No game data found for tomorrow. Skipping update.")
        return

    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
    
    # Extracting game details
    try:
        game = data["dates"][0]["games"][0]
        away_team = game.get("teams", {}).get("away", {}).get("team", {}).get("name", "N/A")
        home_team = game.get("teams", {}).get("home", {}).get("team", {}).get("name", "N/A")
        status = game.get("status", {}).get("detailedState", "Scheduled")
        
        matchup = f"{away_team} @ {home_team}"
        result = status
    except (KeyError, IndexError):
        return

    # Writing to index.html
    html_content = f"""
<html>
<body>
    <h1>Latest MLB Stats</h1>
    <table border="1">
        <tr><th>Matchup</th><th>Result</th></tr>
        <tr><td>{matchup}</td><td>{result}</td></tr>
    </table>
    <p>Last updated: {datetime.now().strftime('%Y-%m-%d')}</p>
</body>
</html>
    """
    
    with open(output_path, "w") as f:
        f.write(html_content)
    print("Successfully updated index.html with tomorrow's game.")

if __name__ == "__main__":
    data = fetch_mlb_data()
    update_html(data)
