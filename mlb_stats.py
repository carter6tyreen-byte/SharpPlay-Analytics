import os
import requests
import json

# 1. Configuration
API_KEY = os.getenv('RAPIDAPI_KEY')
URL = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"
}
QUERYSTRING = {"playerID": "592450"}

def fetch_and_write():
    try:
        # 2. Fetch data
        response = requests.get(URL, headers=HEADERS, params=QUERYSTRING)
        response.raise_for_status()
        data = response.json()
        
        # DEBUG: This will appear in your GitHub Action logs. 
        # Look here to find the actual names of the fields!
        print("DEBUG API RESPONSE:", json.dumps(data, indent=2))
        
        # 3. Extract Data 
        # ADJUST THESE KEYS based on the DEBUG output in your logs
        stats = data.get('body', {})
        matchup = stats.get('matchup', 'N/A')
        result = stats.get('result', 'N/A')
        
        # 4. Generate HTML
        html_content = f"""
        <html>
        <head><title>MLB Stats</title></head>
        <body>
            <h1>Latest Batter vs Pitcher Stats</h1>
            <table border="1">
                <tr><th>Matchup</th><th>Result</th></tr>
                <tr><td>{matchup}</td><td>{result}</td></tr>
            </table>
            <p>Last updated: 2026-07-15</p>
        </body>
        </html>
        """
        
        # 5. Save file
        with open("index.html", "w") as f:
            f.write(html_content)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_write()
