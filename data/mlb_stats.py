import requests
import os

def fetch_mlb_data():
    # Update this with your actual working MLB API endpoint
    url = "https://statsapi.mlb.com/api/v1/schedule/live?sportId=1" 
    headers = {"Authorization": f"Bearer {os.getenv('MLB_API_KEY')}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def update_html(data):
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
    
    matchup = "No Games"
    result = "N/A"
    
    # Updated parsing logic based on standard MLB Stats API structure
    if data and "dates" in data and len(data["dates"]) > 0:
        games = data["dates"][0].get("games", [])
        if len(games) > 0:
            game = games[0]
            away = game.get("teams", {}).get("away", {}).get("team", {}).get("name", "Away")
            home = game.get("teams", {}).get("home", {}).get("team", {}).get("name", "Home")
            status = game.get("status", {}).get("abstractGameState", "Scheduled")
            
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
