import json
import os
from datetime import datetime

def collect_data():
    print("Initializing MLB Data Collector...")
    
    # 1. Structured data
    data = {
        "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "featured_story": {
            "title": "SharpPlay Analytics Active",
            "stat": "System Online",
            "desc": "The predictive engine is running. Data will populate as games are scheduled."
        },
        "matchups": [
            # Example structure:
            # {
            #     "away_team": "Team Name",
            #     "home_team": "Team Name",
            #     "simulated_winner": "Team Name",
            #     "win_probability": "0.0%",
            #     "run_line_proj": "0.0",
            #     "total_runs_proj": "0.0"
            # }
        ]
    }
    
    # Ensure the 'data' directory exists
    output_dir = "data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    file_path = os.path.join(output_dir, "today_matchups.json")
    
    # Write the JSON file
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
        
    print(f"Successfully saved data to {file_path}")

if __name__ == "__main__":
    collect_data()

import sys
import os

# Add the backend folder to your path so Python can find the optimizer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from Starworld_optimizer import run_optimizer # Assuming this is your main function

def collect_data():
    # 1. Run the Starworld Optimizer to get the latest SHADOW values
    print("Running Starworld Optimizer...")
    prediction_results = run_optimizer() 
    
    # 2. Format these results into the JSON structure your site needs
    # (Example mapping logic)
    formatted_data = {
        "last_updated": ..., 
        "matchups": prediction_results
    }
    
    # 3. Write to JSON as you were doing before
    # ...

