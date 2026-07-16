# backend/core_analytics.py

def get_closeness(home_score, away_score):
    return abs(home_score - away_score)

def get_pace(total_runs, inning):
    return round(total_runs / inning, 2) if inning > 0 else 0

def check_alert_threshold(games_data):
    """
    Analyzes a list of games to check for high intensity.
    """
    alerts = []
    
    # Ensure we are iterating through the list correctly
    for game in games_data:
        # Now 'game' is an individual dictionary, so .get() will work
        analytics = game.get("analytics", {})
        
        # Check for your specific threshold logic
        if analytics.get("intensity", 0) > 80:
            alerts.append(game)
            
    return alerts
