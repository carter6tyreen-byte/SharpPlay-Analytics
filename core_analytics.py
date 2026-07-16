# backend/core_analytics.py

def get_closeness(home_score, away_score):
    return abs(home_score - away_score)

def get_pace(total_runs, inning):
    return round(total_runs / inning, 2) if inning > 0 else 0

def check_alert_threshold(game_data):
    """Returns True if the game meets 'high interest' criteria."""
    analytics = game_data.get("analytics", {})
    return analytics.get("intensity") == "High"
