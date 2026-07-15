def run_optimizer():
    """
    Core engine: Analyzes matchups based on the Blast-Contact Matrix.
    Returns a list of simulated results with advanced metrics.
    """
    return [
        {
            "away": "Team A",
            "home": "Team B",
            "predicted_winner": "Team B",
            "prob": 0.65,
            "spread": -1.5,
            "total": 8.5,
            "barrel_score": 77.3
        }
    ]

def calculate_barrel_score(exit_vel, contact_rate):
    # Logic: Normalize to a 100-point scale
    # Assuming exit_vel is 0-120 and contact_rate is 0-1.0
    return round((exit_vel * 0.5) + (contact_rate * 40), 1)

def run_optimizer():
    # Mock data - in the future, this comes from a database or API
    games = [
        {"away": "Team A", "home": "Team B", "ev": 95, "cr": 0.8},
        {"away": "Team C", "home": "Team D", "ev": 105, "cr": 0.65}
    ]
    
    results = []
    for g in games:
        score = calculate_barrel_score(g['ev'], g['cr'])
        results.append({
            "away_team": g['away'],
            "home_team": g['home'],
            "simulated_winner": "Home" if score > 75 else "Away",
            "win_probability": "65%",
            "barrel_score": score
        })
    return results
