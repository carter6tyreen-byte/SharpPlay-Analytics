import requests  # This is the essential fix for your NameError

def run_ingestion():
    """
    Fetches live data from the API endpoint.
    """
    # Ensure your endpoint and headers are defined within your environment or function
    # Example structure:
    # endpoint = "https://your-api-endpoint.com/data"
    # headers = {"Authorization": "Bearer YOUR_TOKEN"}
    
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()  # This will raise an error if the API request fails
        
        data = response.json()
        print("DEBUG: Successfully ingested data from API.")
        return data
        
    except Exception as e:
        print(f"DEBUG: Error during API ingestion: {e}")
        return []

    
    
