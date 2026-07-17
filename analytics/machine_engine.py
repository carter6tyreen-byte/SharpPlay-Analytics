import pandas as pd

class AnalyticsEngine:
    def __init__(self):
        pass

    def run_starworld_optimizer(self, game_id):
        # Your core logic here
        data = {
            'GameID': [game_id],
            'Analysis': ['Value Found'],
            'Confidence': [0.95]
        }
        return pd.DataFrame(data)

def main():
    engine = AnalyticsEngine()
    target_game_id = "823440"
    
    # 1. Run Analysis
    df = engine.run_starworld_optimizer(game_id=target_game_id)
    
    # 2. Convert to HTML directly
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
    
    # 3. Save as index.html
    with open("index.html", "w") as f:
        f.write(html_content)
    print("Optimization complete and index.html updated.")

if __name__ == "__main__":
    main()
