import requests
import os

def run_ingestion():
    """
    Fetches raw data from the API.
    """
    print("DEBUG: Executing run_ingestion...")
    
    # Ensure you have your environment variables set in GitHub Secrets
    url = os.getenv("API_ENDPOINT")
    headers = {
        "x-rapidapi-key": os.getenv("SPORTS_API_KEY"),
        "x-rapidapi-host": os.getenv("API_HOST")
    }
    
    # Perform the request
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    # Return the data to be processed by main.py
    return response.json()

# This ensures that if you run this file directly for testing, it works.
if __name__ == "__main__":
    data = run_ingestion()
    print("Ingestion successful.")
