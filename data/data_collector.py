import requests
import os

def run_ingestion():
    # Defensive programming: Strip all environment variables of hidden junk
    raw_endpoint = os.getenv("API_ENDPOINT", "").strip().replace('\u2060', '')
    raw_key = os.getenv("SPORTS_API_KEY", "").strip().replace('\u2060', '')
    raw_host = os.getenv("API_HOST", "").strip().replace('\u2060', '')

    if not raw_endpoint:
        raise ValueError("API_ENDPOINT is not set or is empty.")

    headers = {
        "x-rapidapi-key": raw_key,
        "x-rapidapi-host": raw_host
    }
    
    print(f"DEBUG: Connecting to {raw_host}...")
    response = requests.get(raw_endpoint, headers=headers)
    response.raise_for_status()
    
    return response.json()
