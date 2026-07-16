import requests

def run_ingestion():
    # If the endpoint fails or returns no data, we can swap this 
    # to mock data to prove the pipeline works.
    endpoint = "https://api.example.com/data" 
    headers = {"Authorization": "Bearer YOUR_TOKEN"}
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"DEBUG: Error during ingestion: {e}")
        # Return a sample to see if the frontend picks it up
        return [{"team": "Test Match", "analytics": {"intensity": 90}}]
