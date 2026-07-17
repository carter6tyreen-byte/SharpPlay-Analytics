import requests
import json

# The 'schedule' endpoint fetches all games for a given date
# Remove specific game IDs from the URL to get the full slate
url = "https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    with open('data/today_matchups.json', 'w') as f:
        json.dump(data, f)
    print("Full slate fetched successfully.")
else:
    print(f"Failed to fetch data: {response.status_code}")
