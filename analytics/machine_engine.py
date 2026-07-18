import pandas as pd
import requests

class AnalyticsEngine:
    def __init__(self):
        # The correct official MLB Stats API base URL
        self.base_url = "https://statsapi.mlb.com/api/v1"
        # No Authorization header is needed for this public API
        self.headers = {} 

    def _fetch_from_api(self, endpoint_type):
        """Fetches data from the MLB public API."""
        try:
            # Construct the full URL (e.g., .../api/v1/people)
            url = f"{self.base_url}/{endpoint_type}"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            print(f"DEBUG: Response status {response.status_code} for {endpoint_type}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching {endpoint_type}: {e}")
            return None
    
    # ... rest of your methods (_process_data, get_pitcher_data, etc.)
