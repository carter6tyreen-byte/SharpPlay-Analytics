import os
import requests
import json
from datetime import date

def fetch_live_mlb_data():
    # RapidAPI settings - update these based on your specific API provider's docs
    # Example URL for a common MLB schedule endpoint
    url = "https://mlb-college-baseball-api.p.rapidapi.com/mlb/matches" 
    
    headers = {
        "x-rapidapi-key": os.getenv("SPORTS_API_KEY"),
        "x-rapidapi-host": "mlb-college-baseball-api.p.rapidapi.com"
    }
    
    # Send the request for today's date
    params = {"date": date.today().isoformat(), "limit": 20}
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def main():
    try:
        live_data = fetch_live_mlb_data()
        
        # Pass the 'live_data' to your existing optimizer
        # You will need to ensure your optimizer processes this specific JSON structure
        optimized_data = run_optimizer(live_data)
        
        with open("data/today_matchups.json", "w") as f:
            json.dump(optimized_data, f, indent=4)
        print("Successfully updated with live data.")
    except Exception as e:
        print(f"Error fetching live data: {e}")

if __name__ == "__main__":
    main()
