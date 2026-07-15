import os
import requests
import json
import sys
# Import from your modules now that they are recognized as packages
from backend.Starworld_optimizer import run_optimizer
from data.data_collector import run_ingestion

def fetch_live_data():
    # Using environment variables (ensure these are set in GitHub Secrets)
    url = os.getenv("API_ENDPOINT") 
    headers = {
        "x-rapidapi-key": os.getenv("SPORTS_API_KEY"),
        "x-rapidapi-host": os.getenv("API_HOST")
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def main():
    try:
        print("Starting pipeline...")
        
        # If your data_collector handles the raw fetching, use that:
        # raw_data = run_ingestion()
        # Otherwise, use your fetch function:
        raw_data = fetch_live_data()
        
        # Pass the live data to your optimizer logic
        optimized_data = run_optimizer(raw_data)
        
        # Save to the JSON file in the data folder
        # Now that main.py is at the root, 'data/today_matchups.json' works perfectly
        with open("data/today_matchups.json", "w") as f:
            json.dump(optimized_data, f, indent=4)
            
        print("Success: Live data fetched, optimized, and saved.")
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
