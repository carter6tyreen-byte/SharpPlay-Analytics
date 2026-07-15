import os
import requests
import json
import sys

# Maintain your path fix to access backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.Starworld_optimizer import run_optimizer

def fetch_live_data():
    url = "https://YOUR-API-ENDPOINT-URL" # Replace with your RapidAPI endpoint
    headers = {
        "x-rapidapi-key": os.getenv("SPORTS_API_KEY"),
        "x-rapidapi-host": "YOUR-API-HOST" # Replace with your host
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def main():
    try:
        live_data = fetch_live_data()
        optimized_data = run_optimizer(live_data)
        with open("data/today_matchups.json", "w") as f:
            json.dump(optimized_data, f, indent=4)
        print("Pipeline Success: Real-time data updated.")
    except Exception as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    main()
