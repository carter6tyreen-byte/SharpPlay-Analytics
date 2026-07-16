# backend/core_analytics.py

def check_alert_threshold(data_to_process):
    """
    Returns ALL data to verify the connection.
    """
    if not isinstance(data_to_process, list):
        return []
        
    # Simply return the list without any filtering
    print(f"DEBUG: Passing through {len(data_to_process)} items.")
    return data_to_process

