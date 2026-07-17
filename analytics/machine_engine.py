import pandas as pd
import json

class AnalyticsEngine:
    def __init__(self):
        # Path relative to the root where the script/app is executed
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
        """Returns optimized data for a specific GameID."""
        target_game = None
        
        # Search through the loaded JSON for the matching GameID
        for date_entry in self.matchup_data.get('dates', []):
            for game in date_entry.get('games', []):
                if str(game.get('gamePk')) == str(game_id):
                    target_game = game
                    break
        
        if not target_game:
            return pd.DataFrame([{"Error": "Game ID not found"}])

        # Placeholder for your optimization logic
        # You can expand this to include actual API math/calculations
        away_team = target_game['teams']['away']['team']['name']
        home_team = target_game['teams']['home']['team']['name']
        status = target_game.get('status', {}).get('detailedState', 'N/A')
        
        data = {
            'Metric': ['Matchup', 'Status', 'Optimization Score'],
            'Value': [
                f"{away_team} at {home_team}", 
                status, 
                "High Value"
            ]
        }
        return pd.DataFrame(data)

# This main block is only for testing the engine independently
if __name__ == "__main__":
    engine = AnalyticsEngine()
    print("Engine initialized and data loaded.")
