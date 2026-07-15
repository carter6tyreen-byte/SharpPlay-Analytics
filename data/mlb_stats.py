import os
import requests
import json

def fetch_mlb_data():
    """
    Fetches MLB game data for 2026-07-15 using the configured API key.
    """
    # Retrieve the API key from the environment variables set in the workflow
    api_key = os.getenv("MLB_API_KEY")
    
    if not api_key:
        print("Error: MLB_API_KEY environment variable is not set.")
        return []

    url = "https://api.sportsdata.io/v3/mlb/scores/json/GamesByDate/2026-07-15"
    headers = {"Ocp-Apim-Subscription-Key": api_key}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Ensure we return a list even if the API response is empty
        return data if isinstance(data, list) else []
        
    except requests.exceptions.RequestException as e:
        print(f"Ingestion Error: {e}")
        return []

if __name__ == "__main__":
    # This allows you to test the script manually by running 'python3 mlb_stats.py'
    data = fetch_mlb_data()
    print(f"Successfully fetched {len(data)} games.")
