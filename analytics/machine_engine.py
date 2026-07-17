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
        # Safely iterate through all date entries in the schedule
        for date_entry in self.matchup_data.get('dates', []):
            for game in date_entry.get('games', []):
                # Using .get() ensures no KeyErrors if data is missing
                away = game.get('teams', {}).get('away', {}).get('team', {}).get('name', 'Unknown')
                home = game.get('teams', {}).get('home', {}).get('team', {}).get('name', 'Unknown')
                
                all_games.append({
                    'GameID': game.get('gamePk'),
                    'Game': f"{away} vs {home}"
                })
        return pd.DataFrame(all_games)

    def run_starworld_optimizer(self, game_id):
        """Locates the specific game and fetches live rosters."""
        target_game = None
        # Locate the specific gamePk within the full slate
        for date_entry in self.matchup_data.get('dates', []):
            for game in date_entry.get('games', []):
                if str(game.get('gamePk')) == str(game_id):
                    target_game = game
                    break
        
        if not target_game:
            return pd.DataFrame([{"Error": "Game ID not found"}])

        # Fetch rosters for both teams in the selected game
        all_players = []
        teams_data = [
            {'team': target_game['teams']['away']['team'], 'side': 'Away'},
            {'team': target_game['teams']['home']['team'], 'side': 'Home'}
        ]
        
        for item in teams_data:
            team_id = item['team']['id']
            team_name = item['team']['name']
            try:
                url = f"https://statsapi.mlb.com/api/v1/teams/{team_id}/roster"
                response = requests.get(url, timeout=5).json()
                for p in response.get('roster', []):
                    all_players.append({
                        'Team': team_name,
                        'Side': item['side'],
                        'Player': p.get('person', {}).get('fullName', 'Unknown'),
                        'Position': p.get('position', {}).get('abbreviation', 'N/A'),
                        'Status': p.get('status', {}).get('description', 'Active')
                    })
            except Exception:
                continue
            
        return pd.DataFrame(all_players) if all_players else pd.DataFrame([{"Message": "Roster data unavailable"}])
