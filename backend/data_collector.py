# backend/data_collector.py

import requests

def run_ingestion():
    # ... your existing code ...
    endpoint = "YOUR_API_URL"
    headers = {"Authorization": "YOUR_TOKEN"}
    
    response = requests.get(endpoint, headers=headers)
    
    # These prints will appear in your GitHub Action logs
    print(f"DEBUG: API status code: {response.status_code}")
    print(f"DEBUG: API response: {response.text}")
    
    return response.json()

