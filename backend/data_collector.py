# In backend/data_collector.py
def run_ingestion():
    # ... after your requests.get(endpoint, headers=headers) call:
    response = requests.get(endpoint, headers=headers)
    
    # DEBUG: Print the raw API response to the logs
    print(f"DEBUG: API Raw Content: {response.text}")
    
    response.raise_for_status()
    return response.json()
