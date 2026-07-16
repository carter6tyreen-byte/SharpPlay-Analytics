import os
import sys

# Since all files are in the root, no complex pathing is needed.
# Direct imports will now work automatically.
from api_client import fetch_sports_data, fetch_market_odds
from data_processor import process_raw_api_data
from prediction_engine import run_hr_prediction_model
from optimizer import get_optimal_bets

def main():
    print("--- SharpPLAY Pipeline Started ---")
    
    try:
        # Retrieve API Key from GitHub Secrets
        api_key = os.getenv("RAPIDAPI_KEY")
        if not api_key:
            raise ValueError("RAPIDAPI_KEY environment variable is not set.")

        # 1. Fetch
        print("Fetching data...")
        raw_data = fetch_sports_data(api_key)
        
        # 2. Process
        print("Processing data...")
        clean_data = process_raw_api_data(raw_data)
        
        # 3. Predict
        print("Running prediction engine...")
        predictions = run_hr_prediction_model(clean_data)
        
        # 4. Optimize
        print("Calculating optimal bets...")
        results = get_optimal_bets(predictions)
        
        print(f"Pipeline Result: {results}")
        print("--- Execution Successful ---")
        
    except Exception as e:
        print(f"Pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
