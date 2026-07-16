import sys
import os

# Ensures the current directory is in the Python search path
sys.path.append(os.getcwd())

from src.api_client import fetch_sports_data

def main():
    print("--- Starting SharpPLAY Daily Workflow ---")
    
    data = fetch_sports_data()
    
    if data:
        print("Success: Data fetched from API.")
        # Future: You will pass 'data' to your Optimizer/Prediction modules here
    else:
        print("Failure: Could not retrieve data.")

if __name__ == "__main__":
    main()
