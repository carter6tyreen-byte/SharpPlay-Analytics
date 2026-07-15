import os
import json
import sys
from datetime import datetime
from backend.Starworld_optimizer import run_optimizer
from data.data_collector import run_ingestion

def main():
    # Verify environment variables exist
    if not all([os.getenv("API_ENDPOINT"), os.getenv("SPORTS_API_KEY"), os.getenv("API_HOST")]):
        print("CRITICAL ERROR: One or more environment variables are missing!")
        sys.exit(1)
    
    try:
        raw_data = run_ingestion()
        optimized_data = run_optimizer(raw_data)
        
        # We explicitly wrap the data to guarantee a predictable structure
        final_payload = {
            "last_updated": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
            "matchups": optimized_data
        }
        
        with open("data/today_matchups.json", "w") as f:
            json.dump(final_payload, f, indent=4)
        print("Data successfully updated.")
            
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
