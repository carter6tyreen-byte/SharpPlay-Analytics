import requests
import json
import os

def fetch_mlb_data():
    # Replace with your actual endpoint and headers
    url = "YOUR_MLB_API_ENDPOINT" 
    headers = {"Authorization": f"Bearer {os.getenv('MLB_API_KEY')}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def update_html(data):
    # Ensure we write to the root 'index.html' from within the 'data/' folder
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
    
    # Simple logic to parse the first game for demonstration
    matchup = "No Game Today"
    result = "N/A"
    
    if data and "games" in data and len(data["games"]) > 0:
        game = data["games"][0]
        matchup = f"{game.get('away_team')} @ {game.get('home_team')}"
        result = game.get('status', 'Final')

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
