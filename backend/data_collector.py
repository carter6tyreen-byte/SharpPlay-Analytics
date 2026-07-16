import requests

def run_ingestion():
    """
    Fetches live data from the API endpoint.
    """
    # Ensure these are defined inside the function or globally
    endpoint = "https://api.example.com/data"  # Replace with your actual endpoint
    headers = {"Authorization": "Bearer YOUR_TOKEN"}
    
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        data = response.json()
        print("DEBUG: Successfully ingested data from API.")
        return data
    except Exception as e:
        print(f"DEBUG: Error during API ingestion: {e}")
        return []
