import requests
import json

def run_ingestion():
    # Variables defined inside the function scope
    endpoint = "https://your-api-url-here.com/data" 
    headers = {"Authorization": "Bearer YOUR_TOKEN"}
    
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        
        # Add a print for debugging in your next run
        print(f"DEBUG: Data successfully fetched: {len(response.text)} bytes.")
        return response.json()
    except Exception as e:
        print(f"DEBUG: Error during ingestion: {e}")
        return []
