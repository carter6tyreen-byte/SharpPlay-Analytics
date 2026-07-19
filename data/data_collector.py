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

for game in schedule:
    game_pk = game.get('game_id')
    if not game_pk:
        continue
    
    try:
        # Get live data or boxscore data safely
        boxscore = statsapi.boxscore_data(game_pk)
        for team_key in ['home', 'away']:
            team_data = boxscore.get(team_key, {})
            players = team_data.get('players', {})
            for player_id, p_info in players.items():
                name = p_info.get('person', {}).get('fullName')
                if name:
                    batting_stats = p_info.get('stats', {}).get('batting', {})
                    pitching_stats = p_info.get('stats', {}).get('pitching', {})
                    
                    player_distributions[name] = {
                        "HR": batting_stats.get('homeRuns', 0),
                        "SO": pitching_stats.get('strikeouts', 0)
                    }
    except Exception as ex:
        print(f"Skipping game {game_pk} due to error: {ex}")

# Fallback: If no players were captured from active boxscores yet, pull team active rosters for today's matchups
if len(player_distributions) == 0:
    print("Boxscores empty or games not started. Pulling from active game rosters...")
    for game in schedule:
        for team_name in [game.get('home_name'), game.get('away_name')]:
            if team_name:
                try:
                    team_id = statsapi.lookup_team(team_name)[0]['id']
                    roster = statsapi.roster(team_id)
                    for line in roster.splitlines():
                        if line.strip():
                            parts = line.split('-')
                            if len(parts) > 1:
                                player_name = parts[1].strip()
                                player_distributions[player_name] = {"HR": 0.0, "SO": 0.0}
                except Exception:
                    pass

# Ensure data directory exists and save
os.makedirs("data", exist_ok=True)
output_path = "data/player_distributions.json"

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(player_distributions, f, indent=4)

print(f"Successfully saved {len(player_distributions)} players to {output_path}.")
