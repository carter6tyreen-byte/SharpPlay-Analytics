import pandas as pd
import requests

class AnalyticsEngine:
    def __init__(self):
        # Ensure your endpoint is correct. Example: "https://api.example.com"
        self.base_url = "YOUR_API_ENDPOINT_HERE"
        self.headers = {"Authorization": "Bearer YOUR_API_KEY"}

    def _fetch_from_api(self, endpoint_type):
        """Fetches data and handles common JSON response structures."""
        try:
            response = requests.get(f"{self.base_url}/{endpoint_type}", headers=self.headers, timeout=10)
            print(f"DEBUG: Response status {response.status_code} for {endpoint_type}")
            
            response.raise_for_status()
            data = response.json()
            
            # Print data to logs to see structure if table remains empty
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
        
        # If data is a dictionary, look for the main list key (common in APIs)
        if isinstance(data, dict):
            # Try to find a key that holds the list (e.g., 'data', 'players', 'stats')
            for key in ['data', 'players', 'stats', 'results']:
                if key in data and isinstance(data[key], list):
                    return pd.DataFrame(data[key])
            # Fallback: normalize the dict
            return pd.json_normalize(data)
            
        # If it's already a list, return as DataFrame
        if isinstance(data, list):
            return pd.DataFrame(data)
            
        return pd.DataFrame()
