import os
import json
import sys
from datetime import datetime
from backend.Starworld_optimizer import run_optimizer
from data.data_collector import run_ingestion

def main():
    # ... (Keep your existing API variable checks)
    
    try:
        raw_data = run_ingestion()
        optimized_data = run_optimizer(raw_data)
        
        # Package data with metadata
        final_payload = {
            "last_updated": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
            "matchups": optimized_data
        }
        
        with open("data/today_matchups.json", "w") as f:
            json.dump(final_payload, f, indent=4)
            
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)
