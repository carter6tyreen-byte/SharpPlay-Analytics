import requests
import os

def fetch_mlb_data():
    # APIs
    endpoints = {
        "schedule": "https://statsapi.mlb.com/api/v1/schedule/live?sportId=1",
        "second_api": "YOUR_SECOND_API_URL_HERE" 
    }
    headers = {"Authorization": f"Bearer {os.getenv('MLB_API_KEY')}"}
    
    results = {}
    for name, url in endpoints.items():
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            results[name] = data
            # PRINTING TO LOGS FOR DEBUGGING
            print(f"DEBUG {name.upper()} DATA: {data}") 
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            results[name] = None
    return results
