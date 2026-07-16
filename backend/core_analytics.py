def check_alert_threshold(data_to_process):
    """
    Debug mode: Bypasses intensity threshold to visualize all incoming data.
    """
    if not isinstance(data_to_process, list):
        print("DEBUG: Data is not a list. Returning empty list.")
        return []
        
    print(f"DEBUG: Pipeline received {len(data_to_process)} items.")
    
    # Bypass logic: Return everything so we can see the data structure 
    # on your dashboard's green RAW DATA block.
    return data_to_process

def get_intensity_score(game_item):
    """
    Helper to extract intensity once we identify the correct key.
    Currently used as a placeholder.
    """
    # Once data appears, look for the correct key (e.g., 'intensity', 'score')
    # and update this return statement accordingly.
    return game_item.get("intensity", 0)
