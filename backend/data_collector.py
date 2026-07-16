import requests

def run_ingestion():
    endpoint = "https://api.example.com/data" # Update with your endpoint
    headers = {"Authorization": "Bearer YOUR_TOKEN"}
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"DEBUG: Error during ingestion: {e}")
        return []
