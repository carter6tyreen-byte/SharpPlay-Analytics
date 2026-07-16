def run_optimizer(data):
    if isinstance(data, dict):
        return data.get("data_points", [])
    return data if isinstance(data, list) else []
