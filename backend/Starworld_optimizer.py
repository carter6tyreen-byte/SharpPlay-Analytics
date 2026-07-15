def run_optimizer(data):
    # 1. Log what we actually got so we can see why it's empty
    print(f"DEBUG: Data received: {data}")
    
    # 2. Safety check: ensure 'dates' exists and is not empty
    dates = data.get("dates", [])
    if not dates:
        print("DEBUG: No dates found in API response.")
        return []
    
    # 3. Safety check: ensure 'games' exists in the first date
    games = dates[0].get("games", [])
    if not games:
        print("DEBUG: No games found for the first date.")
        return []
        
    return games

