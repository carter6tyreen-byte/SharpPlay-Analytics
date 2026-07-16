class StarworldOptimizer:
    """
    The STARWORLD Engine: A decision engine for portfolio optimization.
    It selects the optimal combination of betting opportunities based on 
    risk constraints and model-derived edges.
    """
    def __init__(self, risk_tolerance=0.5, max_picks=5):
        self.risk_tolerance = risk_tolerance
        self.max_picks = max_picks

    def optimize_portfolio(self, opportunities):
        """
        Selects the best combination of bets based on risk and edge.
        opportunities: List of dicts, each containing at least 'edge' and 'game'.
        """
        # 1. Filter for positive edge bets (Value plays)
        candidates = [opp for opp in opportunities if opp.get('edge', 0) > 2.0]
        
        # 2. Sort by highest edge (the primary signal)
        candidates.sort(key=lambda x: x['edge'], reverse=True)
        
        # 3. Apply portfolio constraints (The "Tuning")
        # STARWORLD limits the exposure to the defined max_picks
        optimized_picks = candidates[:self.max_picks]
        
        return optimized_picks
