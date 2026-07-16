import requests
import os

def fetch_sports_data():
    """Fetches sports data from the RapidAPI endpoint."""
    url = "https://sports-information.p.rapidapi.com/mbb/news"
    
    # Store your key in an environment variable on GitHub (Settings > Secrets)
    api_key = os.getenv("RAPIDAPI_KEY") 
    
    headers = {
        "x-rapidapi-host": "sports-information.p.rapidapi.com",
        "x-rapidapi-key": api_key
    }
    
    params = {"limit": "30"}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None
