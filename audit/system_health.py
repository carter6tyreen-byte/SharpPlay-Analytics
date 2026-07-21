import os
import json
import pandas as pd
from datetime import datetime

LOG_FILE = "data/system_health_log.csv"

def log_system_run(success: bool, workflow_name: str, runtime_sec: float, error_message: str = ""):
    """Tracks workflow run success, runtime, and failure causes for reliability audits."""
    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "workflow": workflow_name,
        "success": 1 if success else 0,
        "runtime_sec": round(runtime_sec, 2),
        "error_message": error_message
    }
    
    os.makedirs("data", exist_ok=True)
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
    else:
        df = pd.DataFrame([record])
        
    df.to_csv(LOG_FILE, index=False)

def check_pipeline_health():
    """Calculates success rate and failure trends to monitor developmental milestones."""
    if not os.path.exists(LOG_FILE):
        print("No health logs recorded yet.")
        return 1.0
        
    df = pd.read_csv(LOG_FILE)
    success_rate = df["success"].mean()
    print(f"=== System Reliability Audit ===")
    print(f"Total Runs Tracked: {len(df)}")
    print(f"Successful Workflow %: {success_rate * 100:.1f}%")
    return success_rate

if __name__ == "__main__":
    log_system_run(success=True, workflow_name="Daily Data Pipeline", runtime_sec=14.5)
    check_pipeline_health()
