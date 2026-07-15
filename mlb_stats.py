import requests
import sys
import os

def fetch_mlb_data():
    API_URL = "https://api.sportsdata.io/v3/mlb/scores/json/GamesByDate/2026-07-15"
    
    # Retrieve the key from the environment (injected by GitHub Actions)
    api_key = os.getenv("MLB_API_KEY")
    
    if not api_key:
        print("PIPELINE_ERROR: API Key not found.")
        sys.exit(1)

    headers = {"Ocp-Apim-Subscription-Key": api_key}

    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        print("Successfully ingested MLB data.")
        return response.json()
    except Exception as e:
        print(f"PIPELINE_ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_mlb_data()
