import os
import requests

# Get API Key
key = os.getenv('RAPIDAPI_KEY')

# Define your API Call
url = "https://tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com/getMLBBatterVsPitcher"
headers = {"x-rapidapi-key": key, "x-rapidapi-host": "tank01-mlb-live-in-game-real-time-statistics.p.rapidapi.com"}
querystring = {"playerID": "592450"}

# Execute call
response = requests.get(url, headers=headers, params=querystring).json()

# Generate your HTML string (simplified example)
html_content = f"""
<html>
<body>
    <h1>Latest MLB Stats</h1>
    <p>Data successfully updated!</p>
</body>
</html>
"""

# Write to index.html
with open("index.html", "w") as f:
    f.write(html_content)
