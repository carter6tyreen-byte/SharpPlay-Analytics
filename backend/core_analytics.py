# backend/core_analytics.py
def check_alert_threshold(data_to_process):
    processed = []
    if isinstance(data_to_process, list):
        for game in data_to_process:
            # Add a 'status' field to the game so you can see it on the dashboard
            intensity = game.get("analytics", {}).get("intensity", 0)
            game['is_highlight'] = intensity > 50  # Lowered threshold to see more
            processed.append(game)
    return processed

