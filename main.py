import json
from backend.data_collector import run_ingestion
from backend.Starworld_optimizer import run_optimizer
from backend.core_analytics import check_alert_threshold

def main():
    raw_data = run_ingestion()
    optimized_data = run_optimizer(raw_data)
    alerts = check_alert_threshold(optimized_data)
    
    output = {"payload": {"alerts": alerts, "data_points": optimized_data}}
    with open('data/today_matchups.json', 'w') as f:
        json.dump(output, f)

if __name__ == "__main__":
    main()
