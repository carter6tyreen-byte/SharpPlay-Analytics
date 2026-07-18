import pandas as pd
import requests

class AnalyticsEngine:
    def __init__(self):
        # ... (init code)

    def _process_data(self, data):
        """Converts MLB JSON response into a clean DataFrame with safety checks."""
    
    def get_position_name(code):
        mapping = {
            'P': 'Pitcher', 'C': 'Catcher', '1B': 'First Base', 
            '2B': 'Second Base', '3B': 'Third Base', 'SS': 'Shortstop', 
            'LF': 'Left Field', 'CF': 'Center Field', 'RF': 'Right Field',
            'DH': 'Designated Hitter'
        }
        return mapping.get(code, code)

    def get_all_games(self):
        # 1. Ensure you load your data here first
        # (Assuming you have a function called load_matchup_data() defined elsewhere)
        matchup_data = load_matchup_data() 
        data = matchup_data.get('dates', [])
        
        # 2. Indent the if block properly under the function
        if data is None or not data:
            return pd.DataFrame() 
        
        return pd.DataFrame(data)

    def run_starworld_optimizer(self, game_id):
        # Implementation logic here
        pass
