# backend/data_collector.py

def run_ingestion():
    # ... your existing setup ...
    response = requests.get(endpoint, headers=headers)
    
    # ADD THESE LOGGING LINES:
    print(f"DEBUG: Status Code: {response.status_code}")
    print(f"DEBUG: Response Preview: {response.text[:200]}") # Shows first 200 chars
    
    # ... existing return ...
