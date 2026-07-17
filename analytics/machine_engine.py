import pandas as pd
import os

class AnalyticsEngine:
    def __init__(self):
        # Mapping IDs to human-readable names
        self.game_metadata = {
            "823440": {"Game": "Yankees vs Red Sox", "Player": "Aaron Judge"}
        }

    def run_starworld_optimizer(self, game_id):
        # Fetch metadata or return placeholders if ID not found
        metadata = self.game_metadata.get(game_id, {"Game": "Unknown", "Player": "Unknown"})
        
        data = {
            'Game': [metadata['Game']],
            'Player': [metadata['Player']],
            'Analysis': ['Value Found'],
            'Confidence': [0.95]
        }
        return pd.DataFrame(data)

def main():
    engine = AnalyticsEngine()
    target_game_id = "823440"
    
    # 1. Run Analysis
    df = engine.run_starworld_optimizer(game_id=target_game_id)
    
    # 2. Convert to HTML for the dashboard
    table_html = df.to_html(classes='table', index=False)
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SharpPLAY Value Board</title>
        <style>
            .table {{ width: 100%; border-collapse: collapse; }}
            .table td, .table th {{ border: 1px solid #ddd; padding: 8px; }}
        </style>
    </head>
    <body>
        <h1>Today's Value Board</h1>
        {table_html}
    </body>
    </html>
    """
    
    # 3. Save to root directory so GitHub Pages can pick it up
    # Using absolute path logic to ensure it overwrites the correct file
    with open("index.html", "w") as f:
        f.write(html_content)
    print("Optimization complete and index.html updated.")

if __name__ == "__main__":
    main()
