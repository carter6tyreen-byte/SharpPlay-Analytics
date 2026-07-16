# backend/data_collector.py

import requests

def run_ingestion():
    # ... your existing code ...
    response = requests.get(endpoint, headers=headers)
    
    # This print will appear in your GitHub Action logs
    print(f"DEBUG: API status code: {response.status_code}")
    print(f"DEBUG: API response: {response.text}")
    
    return response.json()
