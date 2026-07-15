import requests
import sys
import os

def fetch_mlb_data():
    API_URL = "https://api.sportsdata.io/v3/mlb/scores/json/GamesByDate/2026-07-15"
    
    # Debugging step: print a masked version of the key to see if it exists
    api_key = os.getenv("MLB_API_KEY")
    
    if not api_key:
        print("PIPELINE_ERROR: API Key not found in environment variables.")
        # This confirms why your pipeline is failing
        sys.exit(1)
    else:
        print("API Key successfully detected.")

    headers = {"Ocp-Apim-Subscription-Key": api_key}

    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        print("Successfully ingested MLB data.")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"PIPELINE_ERROR: Ingestion failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_mlb_data()
