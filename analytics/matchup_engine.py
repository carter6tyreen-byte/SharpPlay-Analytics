def calculate_implied_prob(american_odds):
    return 100 / (american_odds + 100) if american_odds > 0 else abs(american_odds) / (abs(american_odds) + 100)

def analyze_matchups(simulation_results):
    results = []
    for game in simulation_results:
        win_prob = game['simulated_win_prob']
        odds = game['market_odds']
        
        # Calculate Edge (EV)
        decimal_odds = (1 / calculate_implied_prob(odds))
        ev = ((win_prob * decimal_odds) - 1) * 100
        
        results.append({
            "game": game['name'],
            "edge": round(ev, 2),
            "action": "BET" if ev > 2.0 else "PASS"
        })
    return results

class AnalyticsEngine:
    # ... your existing init ...

    @staticmethod
    def calculate_implied_prob(american_odds):
        """Converts American odds to implied probability."""
        if american_odds > 0:
            return 100 / (american_odds + 100)
        return abs(american_odds) / (abs(american_odds) + 100)

    def analyze_matchups(self, simulation_results):
        """
        Processes simulation output to identify betting edges.
        simulation_results: List of dicts with 'simulated_win_prob' and 'market_odds'
        """
        results = []
        for game in simulation_results:
            win_prob = game.get('simulated_win_prob')
            odds = game.get('market_odds')
            
            # Calculate Edge (EV)
            implied_prob = self.calculate_implied_prob(odds)
            decimal_odds = 1 / implied_prob
            ev = ((win_prob * decimal_odds) - 1) * 100
            
            results.append({
                "game": game.get('name'),
                "edge": round(ev, 2),
                "action": "BET" if ev > 2.0 else "PASS"
            })
        return results
