import os
import json
import sys
from datetime import datetime, timedelta

# Import your project-specific modules
from backend.Starworld_optimizer import run_optimizer
from data.data_collector import run_ingestion

def get_timestamp():
    # Adjusting for local time (e.g., EDT is UTC-4)
    local_time = datetime.utcnow() - timedelta(hours=4)
    return local_time.strftime("%Y-%m-%d %I:%M %p")

def main():
    # 1. Environment Validation
    required_vars = ["API_ENDPOINT", "SPORTS_API_KEY", "API_HOST"]
    if not all(os.getenv(var) for var in required_vars):
        print("CRITICAL ERROR: Missing required environment variables.")
        sys.exit(1)
    
    try:
        # 2. Ingestion
        raw_data = run_ingestion()
        
        # 3. Analysis (Transformation Layer)
        # We assume run_optimizer now returns a list of processed objects
        optimized_data = run_optimizer(raw_data)
        
        # 4. Constructing the Unified Schema
        output_payload = {
            "meta": {
                "project_id": "MLB-Live-Analytics",
                "timestamp": get_timestamp(),
                "status": "success"
            },
            "payload": {
                "data_points": optimized_data,
                "analysis_summary": {
                    "count": len(optimized_data),
                    "is_active": len(optimized_data) > 0
                }
            }
        }
        
        # 5. Output
        os.makedirs("data", exist_ok=True)
        with open("data/today_matchups.json", "w") as f:
            json.dump(output_payload, f, indent=4)
            
        print(f"Pipeline executed successfully. Payload count: {len(optimized_data)}")
            
    except Exception as e:
        # Error logging to schema
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
