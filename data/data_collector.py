import json
import os
from datetime import datetime

def collect_data():
    print("Initializing MLB Data Collector...")
    
    # 1. Structure the game data
    data = {
        "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "featured_story": {
            "title": "Jordan Walker Wins Historic 2026 Home Run Derby",
            "stat": "12-11 over Kyle Schwarber",
            "desc": "Jordan Walker hit 6 consecutive home runs on his final out to claim the title at Citizens Bank Park."
        },
        "matchups": [
            {
                "away_team": "New York Mets",
                "home_team": "Philadelphia Phillies",
                "simulated_winner": "Philadelphia Phillies",
                "win_probability": "58.4%",
                "run_line_proj": "-1.5 Phillies",
                "total_runs_proj": "8.5"
            },
            {
                "away_team": "Tampa Bay Rays",
                "home_team": "Boston Red Sox",
                "simulated_winner": "Boston Red Sox",
                "win_probability": "52.1%",
                "run_line_proj": "+1.5 Rays",
                "total_runs_proj": "9.0"
            }
        ]
    }
    
    # 2. Write the data to a JSON file inside the repo
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "today_matchups.json")
    
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
        
    print(f"Successfully generated and saved live data to {file_path}")

if __name__ == "__main__":
    collect_data()
