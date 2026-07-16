import requests # 1. This must be at the very top

def run_ingestion():
    # 2. Use your real API URL here, prefixed with https://
    endpoint = "https://api.your-provider.com/v1/matches" 
    headers = {"Authorization": "YOUR_TOKEN"}
    
    # 3. Print now happens inside the function where 'endpoint' exists
    print(f"DEBUG: Constructing Request to URL: {endpoint}")
    
    response = requests.get(endpoint, headers=headers)
    return response.json()
