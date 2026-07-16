import requests
import json

def run_ingestion():
    endpoint = "YOUR_API_URL_HERE"
    headers = {"Authorization": "YOUR_TOKEN"}
    
    print("DEBUG: Starting API request...")
    try:
        response = requests.get(endpoint, headers=headers)
        # This will print the actual text response to your GitHub Actions logs
        print(f"DEBUG: Response Status Code: {response.status_code}")
        print(f"DEBUG: Response Body: {response.text[:500]}") # First 500 chars
        
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"DEBUG: Critical Error in Ingestion: {str(e)}")
        return []
