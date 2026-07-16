import requests
import os

def run_ingestion():
    """
    Connects to the API and retrieves raw match data with sanitized headers.
    """
    endpoint = os.getenv("API_ENDPOINT")
    api_key = os.getenv("SPORTS_API_KEY")
    api_host = os.getenv("API_HOST")

    if not endpoint or not api_key or not api_host:
        raise ValueError("Missing required API environment variables.")

    # Prepare raw headers
    raw_headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": api_host
    }

    # Sanitize header values to prevent UnicodeEncodeError
    # This removes any non-ASCII characters that might cause encoding failures
    headers = {
        key: str(value).encode('ascii', 'ignore').decode('ascii') 
        for key, value in raw_headers.items()
    }
    
    print("DEBUG: Fetching live data from API with sanitized headers...")
    response = requests.get(endpoint, headers=headers)
    
    # Raise an error if the request fails (e.g., 404, 500)
    response.raise_for_status()
    
    return response.json()
