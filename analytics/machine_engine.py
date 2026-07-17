import pandas as pd
import json

class AnalyticsEngine:
    def __init__(self):
        # Load the live data directly from the JSON file in your data folder
        self.matchup_data = pd.read_json('data/today_matchups.json')

    def run_starworld_optimizer(self):
        # Use the loaded DataFrame instead of a hardcoded dictionary
        # You can now perform your logic on self.matchup_data here
        return self.matchup_data

def main():
    engine = AnalyticsEngine()
    
    # 1. Get the dynamic data
    df = engine.run_starworld_optimizer()
    
    # 2. Convert to HTML
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
    
    # 3. Save to root directory
    with open("index.html", "w") as f:
        f.write(html_content)
    print("Optimization complete using live data.")

if __name__ == "__main__":
    main()
