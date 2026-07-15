import requests
import sys

def fetch_mlb_data():
    # Replace this with your actual secure API endpoint
    API_URL = "https://api.sportsdata.io/v3/mlb/scores/json/GamesByDate/2026-07-15"
    
    # Optional: Include your API Key header if required
    headers = {
        "Ocp-Apim-Subscription-Key": "YOUR_API_KEY_HERE"
    }

    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        
        data = response.json()
        print("Successfully ingested MLB data.")
        return data

    except requests.exceptions.RequestException as e:
        print(f"PIPELINE_ERROR: Stage 1 Ingestion failed: {e}")
        # Exiting with 1 ensures the GitHub Action fails as required
        sys.exit(1)

if __name__ == "__main__":
    fetch_mlb_data()
