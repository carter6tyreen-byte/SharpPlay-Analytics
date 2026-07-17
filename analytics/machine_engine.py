import pandas as pd
import json

class AnalyticsEngine:
    def __init__(self):
        # Point to the data folder at the root level
        with open('data/today_matchups.json', 'r') as f:
            self.matchup_data = json.load(f)

    def run_starworld_optimizer(self):
        all_games = []
        for date_entry in self.matchup_data.get('dates', []):
            for game in date_entry.get('games', []):
                away = game['teams']['away']['team']['name']
                home = game['teams']['home']['team']['name']
                
                all_games.append({
                    'Game': f"{away} vs {home}",
                    'Status': game['status']['detailedState'],
                    'Analysis': 'Value Found'
                })
        return pd.DataFrame(all_games)

def main():
    engine = AnalyticsEngine()
    df = engine.run_starworld_optimizer()
    
    table_html = df.to_html(classes='table', index=False)
    html_content = f"""
    <html>
    <head><title>SharpPLAY Value Board</title></head>
    <body>
        <h1>Today's Value Board</h1>
        {table_html}
    </body>
    </html>
    """
    # Saves index.html at the root
    with open("index.html", "w") as f:
        f.write(html_content)

if __name__ == "__main__":
    main()
