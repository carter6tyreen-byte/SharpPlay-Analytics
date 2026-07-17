import requests
import json

# Fetch today's full schedule
url = "https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    # Save the entire JSON structure
    with open('data/today_matchups.json', 'w') as f:
        json.dump(data, f)
    print("Full slate saved.")
else:
    print(f"Error: {response.status_code}")
git add data/data_collector.py
git commit -m "Updated data_collector to fetch full schedule"
git push
