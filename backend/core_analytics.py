def check_alert_threshold(data_input):
    """
    Analyzes game data to check for high intensity.
    Corrects for data structure variations (list vs dict).
    """
    alerts = []
    
    # 1. Normalize data: Ensure we are always working with a list
    # This prevents the 'AttributeError' by ensuring we can always iterate.
    if isinstance(data_input, dict):
        # If passed a dict, check if it's the wrapper or the object
        data_to_process = data_input.get("data_points", [data_input])
    elif isinstance(data_input, list):
        data_to_process = data_input
    else:
        # Fallback for unexpected types
        return []

    # 2. Iterate safely
    for game in data_to_process:
        # Access nested analytics dict safely
        # .get() on a dictionary is now safe because 'game' is guaranteed to be a dict
        analytics = game.get("analytics", {})
        
        # Check threshold
        if analytics.get("intensity", 0) > 80:
            alerts.append(game)
            
    return alerts
