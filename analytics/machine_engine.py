import pandas as pd
import json
import requests

class AnalyticsEngine:
    def __init__(self):
        # Path relative to the root where Streamlit runs
        try:
            with open('data/today_matchups.json', 'r') as f:
                self.matchup_data = json.load(f)
        except FileNotFoundError:
            self.matchup_data = {"dates": []}

    def get_all_games(self):
        """Returns a DataFrame of all games for the Value Board list."""
        all_games = []
        for date_entry in self.matchup_data.get('dates', []):
            for game in date_entry.get('games', []):
                away = game['teams']['away']['team']['name']
                home = game['teams']['home']['team']['name']
                all_games.append({
                    'GameID': game['gamePk'],
                    'Game': f"{away} vs {home}"
                })
        return pd.DataFrame(all_games)

    def run_starworld_optimizer(self, game_id):
        """Fetches live rosters for the matchup and returns optimized data."""
        # 1. Find the selected game in today_matchups.json
        target_game = None
        for date_entry in self.matchup_data.get('dates', []):
            for game in date_entry.get('games', []):
                if str(game.get('gamePk')) == str(game_id):
                    target_game = game
                    break
        
        if not target_game:
            return pd.DataFrame([{"Error": "Game ID not found"}])

        # 2. Get the away and home team IDs and names
        away_team = target_game['teams']['away']['team']
        home_team = target_game['teams']['home']['team']
        
        teams_to_fetch = [
            {"id": away_team['id'], "name": away_team['name'], "type": "Away"},
            {"id": home_team['id'], "name": home_team['name'], "type": "Home"}
        ]

        all_players = []

        # 3. Fetch actual rosters in real-time from the public MLB API
        for team in teams_to_fetch:
            try:
                url = f"https://statsapi.mlb.com/api/v1/teams/{team['id']}/roster"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    roster_data = response.json().get('roster', [])
                    for player in roster_data:
                        all_players.append({
                            'Team': team['name'],
                            'Side': team['type'],
                            'Player': player.get('person', {}).get('fullName', 'Unknown'),
                            'Position': player.get('position', {}).get('abbreviation', 'N/A'),
                            'Status': player.get('status', {}).get('description', 'Active')
                        })
            except Exception as e:
                # If a request fails, log it and keep going
                continue

        # 4. If no players were loaded, return a fallback message
        if not all_players:
            return pd.DataFrame([{"Message": "No players found or API error occurred."}])

        # 5. Return the full roster data as a clean DataFrame
        return pd.DataFrame(all_players)

# Testing block
if __name__ == "__main__":
    engine = AnalyticsEngine()
    print("Engine testing...")
    # Test with a mock run if data exists
    games = engine.get_all_games()
    if not games.empty:
        first_game_id = games.iloc[0]['GameID']
        print(f"Testing roster fetch for Game ID: {first_game_id}")
        print(engine.run_starworld_optimizer(first_game_id).head())
