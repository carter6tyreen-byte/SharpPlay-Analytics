def check_alert_threshold(games_data):
    # ... your existing normalization ...
    processed = []
    for game in data_to_process:
        analytics = game.get("analytics", {})
        intensity = analytics.get("intensity", 0)

        # Add a 'status' field to the game so you can see it on the frontend
        game['is_alert'] = intensity > 80
        processed.append(game)
    return processed
