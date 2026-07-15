def calculate_implied_prob(american_odds):
    """Converts American odds to decimal probability."""
    if american_odds > 0:
        return 100 / (american_odds + 100)
    else:
        return abs(american_odds) / (abs(american_odds) + 100)

def calculate_ev(win_prob_model, american_odds):
    """
    Calculates Expected Value (EV).
    win_prob_model: Your simulation's win probability (0.0 to 1.0)
    american_odds: The odds provided by the sportsbook
    """
    decimal_odds = (1/calculate_implied_prob(american_odds))
    ev = (win_prob_model * decimal_odds) - 1
    return ev * 100  # Return as percentage

def analyze_matchups(simulation_results):
    """
    Filters games to find +EV opportunities.
    """
    opportunities = []
    for game in simulation_results:
        # Assuming sim_results contains your model's win %
        model_win_prob = game['simulated_win_prob']
        market_odds = game['market_odds']
        
        edge = calculate_ev(model_win_prob, market_odds)
        
        if edge > 2.0:  # Only flag bets with > 2% edge
            opportunities.append({
                "game": game['name'],
                "edge_percent": round(edge, 2),
                "confidence": "HIGH" if edge > 5.0 else "MEDIUM"
            })
    return opportunities
