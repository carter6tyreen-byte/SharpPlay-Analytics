import os
import requests

# Get the key from the environment
key = os.getenv('RAPIDAPI_KEY')

# API Setup
url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
querystring = {"playerID": "592450"}
headers = {
    "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com",
    "x-rapidapi-key": key
}

# Fetch data
response = requests.get(url, headers=headers, params=querystring)
data = response.json()

# Extract data (Adjust keys based on your API's actual response structure)
stats = data.get('body', {})
matchup = stats.get('matchup', 'N/A')
winner = stats.get('winner', 'N/A')

# Create HTML content
html_content = f"""
<html>
<body>
    <h1>Latest Batter vs Pitcher Stats</h1>
    <table border="1">
        <tr><th>Matchup</th><th>Result</th></tr>
        <tr><td>{matchup}</td><td>{winner}</td></tr>
    </table>
    <p>Last updated: 2026-07-15</p>
</body>
</html>
"""

# Overwrite index.html
with open("index.html", "w") as f:
    f.write(html_content)

# Add this right after data = response.json()
print("Full API Response:", data)
