def run_optimizer(data):
    # Instead of filtering, just return the data structure you find
    # This helps verify if the data is arriving at all
    return data.get("dates", [])[0].get("games", [])
