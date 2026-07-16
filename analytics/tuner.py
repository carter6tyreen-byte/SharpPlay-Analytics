import logging

# Set a conservative learning rate (e.g., 0.5%)
LEARNING_RATE = 0.005 

def tune_team_ratings(previous_predictions, actual_results):
    """
    Calculates bias (Predicted vs Actual) and applies a weight adjustment
    to team ratings for the next simulation cycle.
    """
    adjustments = {}
    
    for pred in previous_predictions:
        actual = next((a for a in actual_results if a['game_id'] == pred['game_id']), None)
        
        if actual:
            actual_outcome = 1 if actual['winner'] == 'HOME' else 0
            # Bias = how much we missed by
            bias = pred['win_prob'] - actual_outcome
            
            # Apply adjustment
            # If bias is positive, we are overestimating: reduce home team rating
            adjustment = -bias * LEARNING_RATE
            adjustments[pred['home_team']] = adjustments.get(pred['home_team'], 0) + adjustment
            
            logging.info(f"Tuner: Adjusted {pred['home_team']} by {adjustment:.4f}")
            
    return adjustments
    class StarworldOptimizer:
    def __init__(self, risk_tolerance=0.5, max_picks=5):
        self.risk_tolerance = risk_tolerance # 0 (low risk) to 1 (high risk)
        self.max_picks = max_picks

    def optimize_portfolio(self, opportunities):
        """
        Selects the best combination of bets based on risk and edge.
        """
        # Filter for only positive edge bets
        candidates = [opp for opp in opportunities if opp['edge'] > 2.0]
        
        # Sort by edge (highest first)
        candidates.sort(key=lambda x: x['edge'], reverse=True)
        
        # Apply portfolio constraints (The "Tuning")
        # In the future, this can include correlation checks (e.g., don't pick 
        # two players from the same game if their success is highly correlated)
        optimized_picks = candidates[:self.max_picks]
        
        return optimized_picks

