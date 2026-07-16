import json
from backend.data_collector import run_ingestion
from backend.Starworld_optimizer import run_optimizer
from backend.core_analytics import check_alert_threshold

def main():
    print("DEBUG: Starting pipeline execution...")
    
    # 1. Ingest
    raw_data = run_ingestion()
    
    # 2. Optimize
    optimized_data = run_optimizer(raw_data)
    
    # 3. Analyze
    alerts = check_alert_threshold(optimized_data)
    
    # 4. Save
    output = {"payload": {"alerts": alerts, "data_points": optimized_data}}
    with open('data/today_matchups.json', 'w') as f:
        json.dump(output, f)
    
    print("DEBUG: Pipeline completed successfully.")

if __name__ == "__main__":
    main()
