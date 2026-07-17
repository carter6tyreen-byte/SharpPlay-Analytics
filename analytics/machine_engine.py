import pandas as pd
import requests

class AnalyticsEngine:
    def __init__(self):
        # Add your API base URL or key here if needed
        self.base_url = "YOUR_API_ENDPOINT_HERE"
        self.headers = {"Authorization": "Bearer YOUR_API_KEY"}

    def _fetch_from_api(self, endpoint_type):
        """Internal helper to fetch and validate API data."""
        try:
            # Example API call - replace with your actual request logic
            response = requests.get(f"{self.base_url}/{endpoint_type}")
            response.raise_for_status()
            data = response.json()
            
            # Ensure the returned data is a list of dictionaries
            if isinstance(data, list) and len(data) > 0:
                return data
            return []
        except Exception as e:
            print(f"Error fetching {endpoint_type} data: {e}")
            return []

    def get_pitcher_data(self):
        """Fetches and processes pitcher statistics."""
        data = self._fetch_from_api("pitchers")
        if data:
            df = pd.DataFrame(data)
            return df
        return pd.DataFrame() # Return empty DataFrame if no data

    def get_batter_data(self):
        """Fetches and processes batter statistics."""
        data = self._fetch_from_api("batters")
        if data:
            df = pd.DataFrame(data)
            return df
        return pd.DataFrame() # Return empty DataFrame if no data
