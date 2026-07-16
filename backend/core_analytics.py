def check_alert_threshold(data_to_process):
    """
    Refactored: Bypasses all filtering to visualize incoming API data.
    """
    # Verify we have a list to work with
    if not isinstance(data_to_process, list):
        print("DEBUG: Pipeline Error - data_to_process is not a list.")
        return []
    
    # Log the number of items received to your GitHub Actions run logs
    print(f"DEBUG: Pipeline successfully received {len(data_to_process)} items.")
    
    # RETURN ALL DATA: 
    # By returning the full list without filtering, the data will 
    # populate your dashboard's green RAW DATA block, allowing you 
    # to see the exact keys (e.g., 'intensity', 'impact', 'score').
    return data_to_process

def get_game_metadata(game_item):
    """
    Helper function to be updated once the key structure is confirmed.
    """
    # Once you see the keys in the green box, update this.
    # Example: return game_item.get("team_name", "Unknown")
    return game_item
