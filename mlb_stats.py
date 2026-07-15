import os
import requests

# 1. Get the key
key = os.getenv('RAPIDAPI_KEY')

# 2. Fetch the data
url = "https://your-api-endpoint.com/stats"
headers = {"X-RapidAPI-Key": key}
response = requests.get(url, headers=headers, params=querystring)
print("API Response:", response.json()) # This will show up in your Action logs


# 3. Process the data (Example: assume response is a list of games)
# You will need to loop through your API response to build the rows dynamically
rows = ""
for game in response:
    rows += f"<tr><td>{game['matchup']}</td><td>{game['winner']}</td></tr>"

# 4. Create the HTML string
html_content = f"""
<html>
<body>
    <h1>Latest MLB Stats</h1>
    <table border="1">
        <tr><th>Matchup</th><th>Winner</th></tr>
        {rows}
    </table>
    <p>Last updated: 2026-07-15</p>
</body>
</html>
"""

# 5. Overwrite index.html
with open("index.html", "w") as f:
    f.write(html_content)
