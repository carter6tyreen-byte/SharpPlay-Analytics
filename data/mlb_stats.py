import requests
import os
from datetime import datetime

def fetch_mlb_data():
    # Use today's date to ensure we get active games
    today = datetime.now().strftime("%Y-%m-%d")
    url = f"https://statsapi.mlb.com/api/v1/schedule/live?sportId=1&date={today}"
    
    print(f"DEBUG: Fetching URL: {url}")
    
    try:
        response = requests.get(url)
        print(f"DEBUG: Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            # Verify if there is actually data in the response
            if "dates" in data and len(data["dates"]) > 0:
                print("DEBUG: Data found!")
                return data
            else:
                print("DEBUG: API returned 200 but no games found for today.")
        else:
            print(f"DEBUG: API Error: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")
        
    return None
