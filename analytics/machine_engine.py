import pandas as pd
import requests

class AnalyticsEngine:
    def __init__(self):
        self.base_url = "https://statsapi.mlb.com/api/v1"

    def _process_data(self, data):
        """Converts MLB JSON response into a clean DataFrame."""
        if not data or 'leagueLeaders' not in data:
            return pd.DataFrame()
        # ... (your processing logic)

    # Added 'self' here
    def get_position_name(self, code):
        mapping = {
            'P': 'Pitcher', 'C': 'Catcher', '1B': 'First Base', 
            '2B': 'Second Base', '3B': 'Third Base', 'SS': 'Shortstop', 
            'LF': 'Left Field', 'CF': 'Center Field', 'RF': 'Right Field',
            'DH': 'Designated Hitter'
        }
        return mapping.get(code, code)

    def get_all_games(self):
        # If load_matchup_data is in this class, use self.load_matchup_data()
        matchup_data = self.load_matchup_data() 
        data = matchup_data.get('dates', [])
        
        if not data:
            return pd.DataFrame() 
        
        return pd.DataFrame(data)

    def run_starworld_optimizer(self, game_id):
        pass
