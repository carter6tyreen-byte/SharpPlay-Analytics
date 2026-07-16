import requests
import os

def run_ingestion():
    """
    Connects to the API and retrieves raw match data.
    """
    # Use environment variables to keep your keys secure
    endpoint = os.getenv("API_ENDPOINT")
    api_key = os.getenv("SPORTS_API_KEY")
    api_host = os.getenv("API_HOST")

    if not endpoint or not api_key or not api_host:
        raise ValueError("Missing required API environment variables.")

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": api_host
    }
    
    print("DEBUG: Fetching live data from API...")
    response = requests.get(endpoint, headers=headers)
    
    # Raise an error if the request fails (e.g., 404, 500)
    response.raise_for_status()
    
    return response.json()
