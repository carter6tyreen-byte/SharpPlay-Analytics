import pandas as pd

class AnalyticsEngine:
    def __init__(self):
        # Load the live data
        self.matchup_data = pd.read_json('data/today_matchups.json')

    # Update this line to accept game_id again
    def run_starworld_optimizer(self, game_id):
        # Filter your loaded data for the specific game_id
        # Assuming your JSON has a column named 'GameID'
        result = self.matchup_data[self.matchup_data['GameID'] == int(game_id)]
        return result

def main():
    engine = AnalyticsEngine()
    target_game_id = "823440"
    
    # Now this call will work because the function expects 'game_id'
    df = engine.run_starworld_optimizer(game_id=target_game_id)
    
    # ... rest of your code

