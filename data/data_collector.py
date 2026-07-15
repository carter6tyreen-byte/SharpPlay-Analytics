import os
import requests
import json
import sys

# Maintain the path fix to access the backend module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.Starworld_optimizer import run_optimizer

def fetch_live_data():
    # REPLACE THESE TWO LINES WITH YOUR ACTUAL RAPIDAPI DETAILS
    url = "https://YOUR_API_ENDPOINT_URL_HERE" 
    headers = {
        "x-rapidapi-key": os.getenv("SPORTS_API_KEY"),
        "x-rapidapi-host": "YOUR_API_HOST_HERE"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status() # This will help you debug if the connection fails
    return response.json()

def main():
    try:
        print("Fetching live data...")
        raw_data = fetch_live_data()
        
        # Pass the live data to your optimizer logic
        optimized_data = run_optimizer(raw_data)
        
        # Save to the JSON file your frontend reads
        with open("data/today_matchups.json", "w") as f:
            json.dump(optimized_data, f, indent=4)
        print("Success: Live data fetched, optimized, and saved.")
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

if __name__ == "__main__":
    main()
