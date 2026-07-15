import json
import sys
import os

# Set up path to import from the backend folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.Starworld_optimizer import run_optimizer

def main():
    # Fetch data from the optimizer
    raw_data = run_optimizer()
    
    # Process data to ensure keys match your index.html expectations
    formatted_matchups = []
    for game in raw_data:
        formatted_matchups.append({
            "away_team": game.get("away_team"),      # Ensure this matches 'away_team' in index.html
            "home_team": game.get("home_team"),      # Ensure this matches 'home_team' in index.html
            "simulated_winner": game.get("simulated_winner"), # Ensure this matches
            "win_probability": game.get("win_probability", "0%"),
            "barrel_score": game.get("barrel_score", "N/A")
        })

    # Save to JSON
    output = {"matchups": formatted_matchups}
    with open("data/today_matchups.json", "w") as f:
        json.dump(output, f, indent=4)
    print("Pipeline Success: Data saved.")

if __name__ == "__main__":
    main()
