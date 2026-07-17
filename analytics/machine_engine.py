import pandas as pd
import json

class AnalyticsEngine:
    def __init__(self):
        # Load the JSON data
        with open('data/today_matchups.json', 'r') as f:
            self.matchup_data = json.load(f)

    def run_starworld_optimizer(self, game_id):
        # Traverse the nested structure to find the game
        target_game = None
        for date_entry in self.matchup_data.get('dates', []):
            for game in date_entry.get('games', []):
                if game.get('gamePk') == int(game_id):
                    target_game = game
                    break
        
        if not target_game:
            return pd.DataFrame([{"Error": "Game ID not found"}])

        # Extract names dynamically
        away_team = target_game['teams']['away']['team']['name']
        home_team = target_game['teams']['home']['team']['name']
        
        data = {
            'Game': [f"{away_team} vs {home_team}"],
            'Analysis': ['Value Found'],
            'Confidence': [0.95]
        }
        return pd.DataFrame(data)

def main():
    engine = AnalyticsEngine()
    # The ID passed from your Streamlit input
    target_game_id = "823440"
    
    df = engine.run_starworld_optimizer(game_id=target_game_id)
    
    # Convert to HTML for the dashboard
    table_html = df.to_html(classes='table', index=False)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><title>SharpPLAY Value Board</title></head>
    <body>
        <h1>Today's Value Board</h1>
        {table_html}
    </body>
    </html>
    """
    
    with open("index.html", "w") as f:
        f.write(html_content)

if __name__ == "__main__":
    main()
