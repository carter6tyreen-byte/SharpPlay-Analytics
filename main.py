import os
import sys

# Ensure root is in path
sys.path.append(os.getcwd())

# Use absolute imports
from src import api_client, data_processor, prediction_engine, optimizer

def main():
    print("--- SharpPLAY Pipeline Started ---")
    # Example usage:
    # data = api_client.fetch_sports_data()
    # clean = data_processor.process_raw_api_data(data)
    print("Imports successful. Pipeline is ready.")

if __name__ == "__main__":
    main()
