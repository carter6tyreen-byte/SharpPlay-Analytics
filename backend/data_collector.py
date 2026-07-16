import requests

def run_ingestion():
    # 1. Define the variables here, inside the function
    endpoint = "https://your-api-url-here.com/endpoint" 
    headers = {"Authorization": "Bearer YOUR_TOKEN"}
    
    # 2. Now 'endpoint' and 'headers' are defined and can be used
    response = requests.get(endpoint, headers=headers)
    
    # ... rest of your code ...
    return response.json()
