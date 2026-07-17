import pandas as pd
import requests

class AnalyticsEngine:
    def __init__(self):
        # REPLACE THESE with the actual URL and Key from your data provider
        self.base_url = "https://your-api-domain.com/v1" 
        self.headers = {"Authorization": "Bearer YOUR_REAL_API_KEY_HERE"}

    def _fetch_from_api(self, endpoint_type):
        """Fetches data and handles common JSON response structures."""
        try:
            # Using the headers and base_url defined in __init__
            response = requests.get(f"{self.base_url}/{endpoint_type}", headers=self.headers, timeout=10)
            print(f"DEBUG: Response status {response.status_code} for {endpoint_type}")
            
            response.raise_for_status()
            data = response.json()
            
            # Print structure to help debug if tables remain empty
            print(f"DEBUG: Data structure received: {type(data)}")
            
            return data
        except Exception as e:
            print(f"Error fetching {endpoint_type}: {e}")
            return None

    def get_pitcher_data(self):
        """Fetches and normalizes pitcher data."""
        data = self._fetch_from_api("pitchers")
        return self._process_data(data)

    def get_batter_data(self):
        """Fetches and normalizes batter data."""
        data = self._fetch_from_api("batters")
        return self._process_data(data)

    def _process_data(self, data):
        """Converts various JSON structures into a clean DataFrame."""
        if data is None:
            return pd.DataFrame()
        
        # If data is a dictionary, look for the main list key
        if isinstance(data, dict):
            # Try to find a key that holds the list. 
            # If your API logs show a different key name, add it to this list!
            for key in ['data', 'players', 'stats', 'results', 'response']:
                if key in data and isinstance(data[key], list):
                    return pd.DataFrame(data[key])
            
            # Fallback: normalize the dict into a single-row DataFrame
            return pd.json_normalize(data)
            
        # If it's already a list, return as DataFrame
        if isinstance(data, list):
            return pd.DataFrame(data)
            
        return pd.DataFrame()
