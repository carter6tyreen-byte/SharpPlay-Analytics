import os
import sys
import json

# Force the project root into the Python path
sys.path.insert(0, os.getcwd())

from backend.data_collector import run_ingestion
from backend.Starworld_optimizer import run_optimizer
from backend.core_analytics import check_alert_threshold

def main():
    # 1. Collect Data
    raw_data = run_ingestion()
    
    # 2. Process Data
    optimized_data = run_optimizer(raw_data)
    alerts = check_alert_threshold(optimized_data)
    
    # 3. Structure Final Payload
    final_payload = {
        "alerts": alerts,
        "data_points": optimized_data
    }
    
    # 4. Save to repository (ensuring folder exists)
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "today_matchups.json")
    
    with open(output_path, 'w') as f:
        json.dump({"payload": final_payload}, f)
    
    print(f"Successfully saved data to {output_path}")

if __name__ == "__main__":
    main()
