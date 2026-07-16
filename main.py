import sys
import os

# Ensure the project root is in the path so 'src' is discoverable
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# Now these imports will resolve correctly
try:
    from src.api_client import fetch_sports_data, fetch_market_odds
    from src.data_processor import process_raw_api_data
    from src.prediction_engine import run_hr_prediction_model
    from src.optimizer import get_optimal_bets
except ImportError as e:
    print(f"Import Error: {e}")
    print(f"Current sys.path: {sys.path}")
    sys.exit(1)

def main():
    print("Pipeline initialized successfully.")
    
    # 1. Fetch
    # raw_data = fetch_sports_data()
    # odds = fetch_market_odds()
    
    # 2. Process
    # clean_data = process_raw_api_data(raw_data)
    
    # 3. Predict & Optimize
    # ... logic here ...
    
    print("Pipeline execution complete.")

if __name__ == "__main__":
    main()
