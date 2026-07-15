import requests
import os
import json

def fetch_mlb_data():
    # Use your known endpoint
    url = "https://statsapi.mlb.com/api/v1/schedule/live?sportId=1"
    headers = {"Authorization": f"Bearer {os.getenv('MLB_API_KEY')}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        # This print will appear in your GitHub Action logs
        print("DEBUG_JSON_DATA:", json.dumps(data, indent=2))
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def update_html(data):
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
    
    matchup = "No Games Found"
    result = "N/A"
    
    # Logic: Safely check for the path to the game data
    if data and "dates" in data and len(data["dates"]) > 0:
        games = data["dates"][0].get("games", [])
        if games:
            game = games[0]
            # Adjust these keys based on the DEBUG_JSON_DATA output
            away = game.get("teams", {}).get("away", {}).get("team", {}).get("name", "Away")
            home = game.get("teams", {}).get("home", {}).get("team", {}).get("name", "Home")
            status = game.get("status", {}).get("detailedState", "Scheduled")
            
            matchup = f"{away} @ {home}"
            result = status

    html_content = f"""
<html>
<body>
    <h1>Latest MLB Stats</h1>
    <table border="1">
        <tr><th>Matchup</th><th>Result</th></tr>
        <tr><td>{matchup}</td><td>{result}</td></tr>
    </table>
    <p>Last updated: 2026-07-15</p>
</body>
</html>
    """
    
    with open(output_path, "w") as f:
        f.write(html_content)
    print(f"Successfully wrote data to {output_path}")

if __name__ == "__main__":
    data = fetch_mlb_data()
    update_html(data)
