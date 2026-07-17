import pandas as pd
import json

class AnalyticsEngine:
    def __init__(self):
        # ... your existing __init__ ...
        with open('data/today_matchups.json', 'r') as f:
            self.matchup_data = json.load(f)

    def get_all_games(self):
        # ... your existing get_all_games ...
        # (keep this as is)
        pass

    # --- PASTE THE NEW FUNCTION HERE ---
    def run_starworld_optimizer(self, game_id):
        # 1. Find the specific game object
        target_game = None
        for date_entry in self.matchup_data.get('dates', []):
            for game in date_entry.get('games', []):
                if str(game.get('gamePk')) == str(game_id):
                    target_game = game
                    break
        
        if not target_game:
            return pd.DataFrame([{"Error": "Game ID not found"}])

        # 2. Extract players
        all_players = []
        for team_key in ['away', 'home']:
            team_data = target_game['teams'][team_key]
            # NOTE: Verify if your JSON actually has a 'players' key here!
            # If your JSON structure is different, you must update 'players'
            players = team_data.get('players', {}) 
            for p_id, p_info in players.items():
                all_players.append({
                    'Player': p_info.get('person', {}).get('fullName', 'Unknown'),
                    'Position': p_info.get('position', {}).get('abbreviation', 'N/A'),
                    'Status': 'Optimized'
                })
        
        return pd.DataFrame(all_players)
