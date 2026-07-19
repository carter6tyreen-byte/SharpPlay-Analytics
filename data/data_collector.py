import json
import os
import statsapi
import datetime

today = datetime.date.today().strftime("%Y-%m-%d")
print(f"Fetching full MLB slate for {today}...")

try:
    schedule = statsapi.schedule(date=today)
except Exception as e:
    print(f"Error fetching schedule: {e}")
    schedule = []

player_distributions = {}

# Directly pull from team rosters for all scheduled games today
teams_to_process = set()
for game in schedule:
    if game.get('home_name'):
        teams_to_process.add(game.get('home_name'))
    if game.get('away_name'):
        teams_to_process.add(game.get('away_name'))

print(f"Found {len(teams_to_process)} teams playing today. Fetching rosters...")

for team_name in teams_to_process:
    try:
        team_id = statsapi.lookup_team(team_name)[0]['id']
        roster = statsapi.roster(team_id)
        for line in roster.splitlines():
            if line.strip():
                parts = line.split('-')
                if len(parts) > 1:
                    player_name = parts[1].strip()
                    # Initialize with baseline stats/distributions
                    player_distributions[player_name] = {
                        "HR": 0.08,
                        "SO": 0.20
                    }
    except Exception as ex:
        print(f"Could not fetch roster for {team_name}: {ex}")

# Fallback if no games are scheduled today at all
if len(player_distributions) == 0:
    print("No active slate found, adding default players...")
    player_distributions = {
        "Aaron Judge": {"HR": 0.12, "SO": 0.25},
        "Shohei Ohtani": {"HR": 0.1, "SO": 0.2}
    }

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "data")
os.makedirs(data_dir, exist_ok=True)
output_path = os.path.join(data_dir, "player_distributions.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(player_distributions, f, indent=4)

print(f"Successfully saved {len(player_distributions)} players to {output_path}.")
