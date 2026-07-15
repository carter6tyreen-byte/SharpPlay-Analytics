import json
import sys
import os

# Set up path to import from the backend folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.Starworld_optimizer import run_optimizer

def main():
    # Fetch data
    raw_data = run_optimizer()
    
    # Process data
    formatted_matchups = []
    for game in raw_data:
        formatted_matchups.append({
            "away_team": game.get("away"),
            "home_team": game.get("home"),
            "simulated_winner": game.get("predicted_winner"),
            "win_probability": f"{int(game.get('prob', 0) * 100)}%",
            "barrel_score": game.get("barrel_score", "N/A")
        })

    # Save to JSON
    output = {"matchups": formatted_matchups}
    with open("data/today_matchups.json", "w") as f:
        json.dump(output, f, indent=4)
    print("Pipeline Success: Data saved.")

if __name__ == "__main__":
    main()
    # Ensure these keys match your JavaScript precisely
formatted_matchups.append({
    "away_team": game.get("away"),    # Must match m.away_team in JS
    "home_team": game.get("home"),    # Must match m.home_team in JS
    "simulated_winner": game.get("predicted_winner"), # Must match m.simulated_winner
    "win_probability": f"{int(game.get('prob', 0) * 100)}%",
    "barrel_score": game.get("barrel_score", "N/A")
})

