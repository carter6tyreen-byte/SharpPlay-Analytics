import requests
import json
import os

def run_ingestion():
    # 1. Configuration - Replace with your actual credentials
    # Ensure these are stored as GitHub Secrets in a real environment
    API_URL = "https://YOUR_API_ENDPOINT_HERE"
    HEADERS = {"Authorization": "Bearer YOUR_TOKEN_HERE"}
    
    print(f"DEBUG: Starting ingestion process to: {API_URL}")

    try:
        # 2. Fetch Data
        response = requests.get(API_URL, headers=HEADERS, timeout=10)
        
        # 3. Log Status for Debugging
        print(f"DEBUG: API returned Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if the list is empty
            if not data:
                print("WARNING: API returned a successful 200, but the list is empty [].")
                return []
            
            print(f"DEBUG: Successfully retrieved {len(data)} items.")
            return data
        else:
            print(f"ERROR: API request failed with status {response.status_code}")
            return []

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Connection to API failed: {e}")
        return []

if __name__ == "__main__":
    # This block executes when the script runs directly
    results = run_ingestion()
    
    # Save the result to a file for your frontend
    output_path = "data/today_matchups.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(results, f)
    
    print(f"SUCCESS: Data saved to {output_path}")
