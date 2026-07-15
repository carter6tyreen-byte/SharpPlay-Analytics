import os
import json
import requests
import sys

# Ensure backend can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.Starworld_optimizer import run_optimizer

def fetch_live_matchups():
    # Retrieve the secret from the environment (set in GitHub Actions YAML)
    api_key = os.getenv("SPORTS_API_KEY")
    
    # Example structure for an API request - update the URL to your provider's docs
    url = "https://api.your-provider.com/v1/mlb/matchups"
    headers = {"x-api-key": api_key}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Check for HTTP errors
        return response.json()
    except Exception as e:
        print(f"API Error: {e}")
        return [] # Return empty list if fetch fails

def main():
    # 1. Fetch live data
    raw_api_data = fetch_live_matchups()
    
    # 2. Process data through your optimizer
    # (Assuming run_optimizer can now take 'raw_api_data' as an argument)
    optimized_data = run_optimizer(raw_api_data)
    
    # 3. Save the output
    output = {"matchups": optimized_data}
    with open("data/today_matchups.json", "w") as f:
        json.dump(output, f, indent=4)
    print("Pipeline Success: Real-time data saved.")

if __name__ == "__main__":
    main()
