import os
import json
import sys
from backend.Starworld_optimizer import run_optimizer
from data.data_collector import run_ingestion

def main():
    # Debugging: Print these to the GitHub Actions logs to verify they are loaded
    api_url = os.getenv("API_ENDPOINT")
    api_key = os.getenv("SPORTS_API_KEY")
    api_host = os.getenv("API_HOST")
    
    print(f"DEBUG: API_ENDPOINT: '{api_url}'")
    print(f"DEBUG: API_HOST: '{api_host}'")
    
    if not api_url or not api_key or not api_host:
        print("CRITICAL ERROR: One or more environment variables are missing!")
        sys.exit(1)

    try:
        print("Starting pipeline...")
        # Fetch the data
        raw_data = run_ingestion()
        
        # Pass the data to your optimizer
        optimized_data = run_optimizer(raw_data)
        
        # Save to the JSON file
        with open("data/today_matchups.json", "w") as f:
            json.dump(optimized_data, f, indent=4)
            
        print("Success: Live data fetched, optimized, and saved.")
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
