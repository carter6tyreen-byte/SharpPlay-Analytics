import json
import os
from backend.data_collector import run_ingestion
from backend.Starworld_optimizer import run_optimizer
from backend.core_analytics import check_alert_threshold

def main():
    # 1. Collect Data
    raw_data = run_ingestion()
    
    # 2. Optimize Data
    optimized_data = run_optimizer(raw_data)
    
    # 3. Analyze Data
    alerts = check_alert_threshold(optimized_data)
    
    # 4. Save Data to the Root 'data' folder
    output_dir = 'data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, 'today_matchups.json')
    
    output = {"payload": {"alerts": alerts, "data_points": optimized_data}}
    
    with open(output_path, 'w') as f:
        json.dump(output, f)
        print(f"DEBUG: Successfully wrote {len(optimized_data)} items to {output_path}")

if __name__ == "__main__":
    main()
