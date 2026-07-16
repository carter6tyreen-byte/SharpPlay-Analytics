from src.api_client import fetch_sports_data
# Import other phases as you build them
# from src.prediction_engine import run_models
# from src.optimizer import run_optimizer

def main():
    print("--- Starting SharpPLAY Daily Workflow ---")
    
    # 1. Collect Data (Phase 2 & 5)
    print("Fetching data from API...")
    data = fetch_sports_data()
    
    if data:
        print("Data successfully retrieved.")
        # 2. Run Prediction & Optimizer (Phase 3 & 4)
        # result = run_models(data)
        # run_optimizer(result)
        
        print("Workflow completed successfully.")
    else:
        print("Failed to retrieve data. Check API connection.")

if __name__ == "__main__":
    main()
