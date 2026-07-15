import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now the import will work
from backend.Starworld_optimizer import run_optimizer

import os
import requests
import json
from backend.Starworld_optimizer import run_optimizer

def fetch_live_mlb_data():
    # Use the endpoint URL from your RapidAPI dashboard
    url = "https://mlb-data.p.rapidapi.com/v1/games" 
    headers = {
        "x-rapidapi-key": os.getenv("SPORTS_API_KEY"),
        "x-rapidapi-host": "mlb-data.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def main():
    try:
        raw_data = fetch_live_mlb_data()
        # Process through your optimizer
        optimized_data = run_optimizer(raw_data)
        
        # Save for your frontend
        with open("data/today_matchups.json", "w") as f:
            json.dump(optimized_data, f, indent=4)
        print("Success: Live data fetched and optimized.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
