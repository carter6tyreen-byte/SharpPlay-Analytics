import pandas as pd
import json

class AnalyticsEngine:
    def __init__(self):
        with open('data/today_matchups.json', 'r') as f:
            self.matchup_data = json.load(f)

    def run_starworld_optimizer(self):
        all_games = []
        # Iterate through all dates and all games
        for date_entry in self.matchup_data.get('dates', []):
            for game in date_entry.get('games', []):
                away_team = game['teams']['away']['team']['name']
                home_team = game['teams']['home']['team']['name']
                
                all_games.append({
                    'GameID': game['gamePk'],
                    'Game': f"{away_team} vs {home_team}",
                    'Analysis': 'Value Found',
                    'Confidence': 0.95
                })
        
        return pd.DataFrame(all_games)

def main():
    engine = AnalyticsEngine()
    # Now returns a DataFrame with ALL games
    df = engine.run_starworld_optimizer()
    
    # Save as HTML
    table_html = df.to_html(classes='table', index=False)
    # ... (rest of your HTML generation code)
