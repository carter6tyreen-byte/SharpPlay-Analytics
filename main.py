import sys
import os
# This forces Python to recognize the root directory
sys.path.append(os.getcwd())

# Now your existing imports will work
from src.api_client import fetch_sports_data, fetch_market_odds
from src.data_processor import process_raw_api_data
from src.prediction_engine import run_hr_prediction_model
from src.optimizer import get_optimal_bets

# ... rest of your main logic ...

import sys
import os
# This forces Python to recognize the root directory
sys.path.append(os.getcwd())

# Now your existing imports will work
from src.api_client import fetch_sports_data, fetch_market_odds
from src.data_processor import process_raw_api_data
from src.prediction_engine import run_hr_prediction_model
from src.optimizer import get_optimal_bets

# ... rest of your main logic ...
rom src.data_processor import process_raw_api_data
import os
from src.api_client import fetch_sports_data, fetch_market_odds
from src.data_processor import process_raw_api_data
from src.prediction_engine import run_hr_prediction_model
from src.optimizer import get_optimal_bets

def main():
    print("--- Starting SharpPLAY Daily Workflow ---")
    
    # 1. Fetch
    print("Fetching raw data and market odds...")
    raw_data = fetch_sports_data()
    market_odds = fetch_market_odds() # Ensure this function exists in api_client
    
    if not raw_data or not market_odds:
        print("Failure: Could not retrieve necessary data or odds.")
        return

    # 2. Process
    print("Processing and cleaning data...")
    clean_data = process_raw_api_data(raw_data)
    
    # 3. Predict
    print("Running HR Prediction Engine...")
    # Assume run_hr_prediction_model returns a dict of {player_name: probability}
    predictions = run_hr_prediction_model(clean_data)
    
    # 4. Optimize
    print("Calculating Expected Value (EV)...")
    final_plays = get_optimal_bets(predictions, market_odds)
    
    # 5. Output
    print("\n--- SHARPPLAY OPTIMIZED PLAYS ---")
    if not final_plays:
        print("No positive EV plays found for today.")
    else:
        for play in final_plays:
            print(f"| Player: {play['player']:<20} | Edge: {play['ev']*100:>6.2f}% |")
    print("----------------------------------\n")

if __name__ == "__main__":
    main()
