import os
import requests

# 1. Get the key
key = os.getenv('RAPIDAPI_KEY')

# 2. Fetch the data
url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
headers = {"x-rapidapi-key": key, "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"}
querystring = {"playerID": "592450"}

response = requests.get(url, headers=headers, params=querystring).json()
print("API DEBUG DATA:", data)

# 3. Extract your data (This assumes the API returns a 'body' dictionary)
# Note: Check your logs if this returns N/A to find the exact key names!
stats = response.get('body', {})
matchup = stats.get('matchup', 'N/A')
winner = stats.get('winner', 'N/A')

# 4. Generate the HTML with live variables
html_content = f"""
<html>
<body>
    <h1>Latest MLB Stats</h1>
    <table border="1">
        <tr><th>Matchup</th><th>Result</th></tr>
        <tr><td>{matchup}</td><td>{winner}</td></tr>
    </table>
    <p>Last updated: 2026-07-15</p>
</body>
</html>
"""

# 5. Save and Push
with open("index.html", "w") as f:
    f.write(html_content)
