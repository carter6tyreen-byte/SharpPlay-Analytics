import os
import requests
import json
import sys
# Now that your folders are packages, these imports will work natively
from backend.Starworld_optimizer import run_optimizer
from data.data_collector import run_ingestion

def fetch_live_data():
    # Keep using environment variables for security
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
        # Fetch the data
        raw_data = fetch_live_data()
        
        # Pass the data to your optimizer
        optimized_data = run_optimizer(raw_data)
        
        # Save to the JSON file
        # Since main.py is in the root, this path is now correct
        with open("data/today_matchups.json", "w") as f:
            json.dump(optimized_data, f, indent=4)
            
        print("Success: Live data fetched, optimized, and saved.")
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1) # Ensure the pipeline fails if the script fails

if __name__ == "__main__":
    main()
