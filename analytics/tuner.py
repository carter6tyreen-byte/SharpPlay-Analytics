def adjust_team_ratings(brier_performance_data):
    """
    If the Brier Score indicates consistent error, 
    nudge the team ratings for the next day's simulation.
    """
    for team, stats in brier_performance_data.items():
        # If your prediction was too high (model is overestimating team strength)
        if stats['avg_prediction_error'] > 0.1:
            # Apply a 2% penalty to offensive rating
            stats['offense_rating'] *= 0.98
            logging.info(f"Calibration: Adjusted {team} offense rating down.")
            
        # If your prediction was too low (model is underestimating team strength)
        elif stats['avg_prediction_error'] < -0.1:
            # Boost offensive rating
            stats['offense_rating'] *= 1.02
            logging.info(f"Calibration: Adjusted {team} offense rating up.")
            
    return brier_performance_data
