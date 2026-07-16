import os
import json
import sys
from datetime import datetime, timedelta

# Import analytical tools from your new package structure
from backend import run_ingestion, run_optimizer, check_alert_threshold

def get_timestamp():
    local_time = datetime.utcnow() - timedelta(hours=4)
    return local_time.strftime("%Y-%m-%d %I:%M %p")

def main():
    # 1. Environment Validation
    required_vars = ["API_ENDPOINT", "SPORTS_API_KEY", "API_HOST"]
    if not all(os.getenv(var) for var in required_vars):
        print("CRITICAL ERROR: Missing environment variables.")
        sys.exit(1)
    
    try:
        # 2. Pipeline Execution
        raw_data = run_ingestion()
        optimized_data = run_optimizer(raw_data)
        
        # 3. Alerting Logic (The "Active" Monitor)
        alerts = [game for game in optimized_data if check_alert_threshold(game)]
        
        # 4. Constructing the Unified Schema
        output_payload = {
            "meta": {
                "project_id": "MLB-Live-Analytics",
                "timestamp": get_timestamp(),
                "status": "success"
            },
            "payload": {
                "data_points": optimized_data,
                "alerts": alerts
            }
        }
        
        # 5. Output
        os.makedirs("data", exist_ok=True)
        with open("data/today_matchups.json", "w") as f:
            json.dump(output_payload, f, indent=4)
            
        print(f"Pipeline success. Games: {len(optimized_data)}, Alerts: {len(alerts)}")
            
    except Exception as e:
        error_payload = {
            "meta": {"status": "error", "timestamp": get_timestamp()},
            "payload": {"error": str(e)}
        }
        with open("data/today_matchups.json", "w") as f:
            json.dump(error_payload, f, indent=4)
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
