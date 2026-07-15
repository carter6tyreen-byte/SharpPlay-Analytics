import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.Starworld_optimizer import run_optimizer

def main():
    raw_data = run_optimizer()
    
    # Map raw engine data to your JSON structure
    formatted_matchups = []
    for game in raw_data:
        formatted_matchups.append({
            "away_team": game.get("away"),
            "home_team": game.get("home"),
            "simulated_winner": game.get("predicted_winner"),
            "win_probability": f"{int(game.get('prob', 0) * 100)}%",
            "run_line_proj": str(game.get("spread")),
            "total_runs_proj": str(game.get("total"))
        })

    output = {
        "last_updated": "2026-07-14 22:20:00 UTC",
        "featured_story": {"title": "System Online", "stat": "V2.2", "desc": "Ready."},
        "matchups": formatted_matchups
    }

    with open("data/today_matchups.json", "w") as f:
        json.dump(output, f, indent=4)

if __name__ == "__main__":
    main()
# Inside your loop in data_collector.py
formatted_matchups.append({
    "away_team": game.get("away"),
    "home_team": game.get("home"),
    "simulated_winner": game.get("predicted_winner"),
    "win_probability": f"{int(game.get('prob', 0) * 100)}%",
    "barrel_score": game.get("barrel_score") # Map it here
})

