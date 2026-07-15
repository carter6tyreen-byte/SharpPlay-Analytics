import random

def run_game(home_stats, away_stats):
    """
    Simulates one full game iteration based on team performance metrics.
    home_stats: Dictionary containing batting/pitching averages, barrel rates, etc.
    away_stats: Dictionary containing opponent metrics.
    """
    home_score = 0
    away_score = 0
    
    # Simple logic: Generate score based on a normal distribution 
    # centered on their season-average production.
    # In a pro system, replace this with at-bat by at-bat simulation.
    home_score = max(0, int(random.normalvariate(home_stats['avg_runs'], 1.5)))
    away_score = max(0, int(random.normalvariate(away_stats['avg_runs'], 1.5)))
    
    return "HOME" if home_score > away_score else "AWAY"

def run_monte_carlo(data, iterations=5000):
    """
    Runs the simulation loop and returns the win probability.
    """
    home_wins = 0
    
    for _ in range(iterations):
        result = run_game(data['home'], data['away'])
        if result == "HOME":
            home_wins += 1
            
    return home_wins / iterations
