import numpy as np
import logging

class MonteCarloSimulator:
    def __init__(self, iterations=10000):
        self.iterations = iterations
        logging.basicConfig(level=logging.INFO)

    def _simulate_game(self, home_stats, away_stats):
        """
        Uses Poisson distribution to simulate runs based on team offensive 
        production and defensive pitching strength.
        """
        # Calculate expected runs (lambda)
        # Expected = (Offense Strength + Opponent Pitcher Weakness) / 2
        home_exp = (home_stats['offense_rating'] + away_stats['pitcher_rating']) / 2
        away_exp = (away_stats['offense_rating'] + home_stats['pitcher_rating']) / 2
        
        home_score = np.random.poisson(home_exp)
        away_score = np.random.poisson(away_exp)
        
        return 1 if home_score > away_score else 0

    def run(self, games_data):
        """
        Expects games_data to be a list of dictionaries containing home/away stats.
        """
        results = []
        for game in games_data:
            home_wins = 0
            
            for _ in range(self.iterations):
                home_wins += self._simulate_game(game['home'], game['away'])
            
            win_prob = home_wins / self.iterations
            
            results.append({
                "game_id": game['game_id'],
                "simulated_win_prob": win_prob,
                "market_odds": game['market_odds']
            })
            
        return results

# Explanation of the math:
# The Poisson distribution assumes events (runs) happen independently at a constant rate.
# 
