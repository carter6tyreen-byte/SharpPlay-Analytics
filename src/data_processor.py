import logging

def process_matchup_data(raw_data):
    """
    Transforms raw scraped data into a structured dictionary of features.
    """
    logging.info("Transforming raw data into features...")
    processed_features = {}
    
    # Example logic: ensure raw_data is iterable
    if not isinstance(raw_data, dict):
        raise ValueError("Raw data must be a dictionary.")

    for game_id, details in raw_data.items():
        # Clean and extract features here
        processed_features[game_id] = {
            "player": details.get("player", "unknown"),
            "opponent": details.get("opponent", "unknown"),
            "odds": details.get("odds", 0.0),
            "status": "processed"
        }
    
    return processed_features
