# backend/core_analytics.py

def check_alert_threshold(data_to_process):
    """
    Filters incoming game data and returns list of high-intensity alerts.
    """
    alerts = []
    
    # Ensure data_to_process is a list
    if not isinstance(data_to_process, list):
        print(f"DEBUG: Data format issue. Received: {type(data_to_process)}")
        return []

    for game in data_to_process:
        # Safely extract intensity, defaulting to 0 if missing
        analytics = game.get("analytics", {})
        intensity = analytics.get("intensity", 0)
        
        # Threshold logic
        if intensity > 80:
            alerts.append(game)
            
    print(f"DEBUG: Filtered {len(alerts)} alerts from {len(data_to_process)} games.")
    return alerts
