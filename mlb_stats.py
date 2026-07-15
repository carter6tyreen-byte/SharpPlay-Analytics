import os
import requests

# 1. Get the key
key = os.getenv('RAPIDAPI_KEY')

# 2. Fetch the data (Replace this URL with your actual API endpoint)
url = "https://your-api-endpoint.com/stats"
headers = {"X-RapidAPI-Key": key}
# response = requests.get(url, headers=headers).json()

# 3. Create the HTML string (Example table)
html_content = f"""
<html>
<body>
    <h1>Latest MLB Stats</h1>
    <table border="1">
        <tr><th>Matchup</th><th>Winner</th></tr>
        <tr><td>Team A @ Team B</td><td>Home</td></tr>
    </table>
    <p>Last updated: 2026-07-15</p>
</body>
</html>
"""

# 4. Overwrite index.html
with open("index.html", "w") as f:
    f.write(html_content)
