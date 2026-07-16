from src.api_client import fetch_sports_data
from src.data_processor import process_raw_api_data
from src.prediction_engine import run_hr_prediction_model

def main():
    print("--- Starting SharpPLAY Daily Workflow ---")
    
    # 1. Fetch
    raw_data = fetch_sports_data()
    
    if raw_data:
        # 2. Process (The step you just added)
        clean_data = process_raw_api_data(raw_data)
        print("Data processed successfully.")
        
        # 3. Predict
        results = run_hr_prediction_model(clean_data)
        print(f"Prediction complete: {results}")
    else:
        print("Failure: Could not retrieve data.")

if __name__ == "__main__":
    main()
