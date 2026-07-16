import os
import json
import os
import sys

# --- ADD THIS BLOCK ---
# This forces the current directory to be recognized as a package root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
# -----------------------

import json
from datetime import datetime, timedelta

from backend.Starworld_optimizer import run_optimizer
from backend.core_analytics import check_alert_threshold
from backend.data_collector import run_ingestion

import sys
from datetime import datetime, timedelta

# Import your tools from the backend package
# Ensure these files exist in your backend/ directory
from backend.Starworld_optimizer import run_optimizer
from backend.core_analytics import check_alert_threshold
# Replace 'data_collector' with the actual filename where your ingestion logic resides
from backend.data_collector import run_ingestion 

def get_timestamp():
    # Adjusted for your local environment
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
        
        # 3. Alerting Logic
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
