import pandas as pd
import json
import requests

class AnalyticsEngine:
    def __init__(self):
        # Load the full slate of games from the collected JSON
        try:
            with open('data/today_matchups.json', 'r') as f:
                self.matchup_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.matchup_data = {"dates": []}

    def get_all_games(self):
        """Extracts every game from the full slate of dates."""
        all_games = []
        # Iterate through all dates to catch every game scheduled
        for date_entry in self.matchup_data.get('dates', []):
            for game in date_entry.get('games', []):
                away = game.get('teams', {}).get('away', {}).get('team', {}).get('name', 'Unknown')
                home = game.get('teams', {}).get('home', {}).get('team', {}).get('name', 'Unknown')
                
                # Format clearly for the UI: "Team A at Team B"
                all_games.append({
                    'GameID': game.get('gamePk'),
                    'Game': f"{away} at {home}"
                })
        return pd.DataFrame(all_games)

    def run_starworld_optimizer(self, game_id):
        """Locates the specific game and fetches full rosters for BOTH teams."""
        target_game = None
        for date_entry in self.matchup_data.get('dates', []):
            for game in date_entry.get('games', []):
                if str(game.get('gamePk')) == str(game_id):
                    target_game = game
                    break
        
        if not target_game:
            return pd.DataFrame([{"Error": "Game ID not found"}])

        all_players = []
        # Define both teams to ensure we fetch both rosters
        teams_to_fetch = [
            {'id': target_game['teams']['away']['team']['id'], 'name': target_game['teams']['away']['team']['name'], 'side': 'Away'},
            {'id': target_game['teams']['home']['team']['id'], 'name': target_game['teams']['home']['team']['name'], 'side': 'Home'}
        ]
        
        for t in teams_to_fetch:
            try:
                url = f"https://statsapi.mlb.com/api/v1/teams/{t['id']}/roster"
                response = requests.get(url, timeout=5).json()
                for p in response.get('roster', []):
                    all_players.append({
                        'Team': t['name'],
                        'Side': t['side'],
                        'Player': p.get('person', {}).get('fullName', 'Unknown'),
                        'Position': p.get('position', {}).get('abbreviation', 'N/A'),
                        'Status': p.get('status', {}).get('description', 'Active')
                    })
            except Exception:
                continue
            
        return pd.DataFrame(all_players) if all_players else pd.DataFrame([{"Message": "Roster data unavailable"}])
