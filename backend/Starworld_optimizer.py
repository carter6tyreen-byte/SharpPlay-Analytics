def run_optimizer(data):
    """
    Processes the raw API data and extracts dates.
    """
    # Check if the data is a dictionary before trying to call .get()
    if isinstance(data, dict):
        dates = data.get("dates", [])
    elif isinstance(data, list):
        # If the API returns a list, use it directly
        dates = data
    else:
        print(f"DEBUG: Unexpected data format: {type(data)}")
        dates = []
    
    # ... your existing optimization logic here
    print(f"DEBUG: Optimizer processed {len(dates)} dates.")
    return dates
