import datetime
import json
import os
import requests

# Calculate tomorrow's date
tomorrow_date = (
    datetime.date.today() + datetime.timedelta(days=1)
).strftime("%Y-%m-%d")

# Example API call structure to MLB Stats API for schedule & probable pitchers
url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={tomorrow_date}&hydrate=probablePitcher,lineups"
response = requests.get(url)
data = response.json()

games_list = []
for date_entry in data.get("dates", []):
  for game in date_entry.get("games", []):
    games_list.append({
        "game_pk": game.get("gamePk"),
        "game_time": game.get("gameDate"),
        "away_team": game.get("teams", {}).get("away", {}).get("team", {}).get("name"),
        "home_team": game.get("teams", {}).get("home", {}).get("team", {}).get("name"),
        "away_probable_pitcher": game.get("teams", {}).get("away", {}).get("probablePitcher", {}).get("fullName", "TBD"),
        "home_probable_pitcher": game.get("teams", {}).get("home", {}).get("probablePitcher", {}).get("fullName", "TBD"),
    })

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Save out to the exact path your Streamlit app is looking for
output_path = f"data/slate_{tomorrow_date}.json"
with open(output_path, "w") as f:
  json.dump(games_list, f, indent=4)
