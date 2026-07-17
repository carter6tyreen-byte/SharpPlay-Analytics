import pandas as pd
import requests

class AnalyticsEngine:
    def __init__(self):
        self.base_url = "YOUR_API_ENDPOINT_HERE"
        self.headers = {"Authorization": "Bearer YOUR_API_KEY"}

    # --- PLACE THE NEW METHOD HERE ---
    def _fetch_from_api(self, endpoint_type):
        """Internal helper to fetch and validate API data."""
        try:
            response = requests.get(f"{self.base_url}/{endpoint_type}")
            
            # These are the lines you requested for debugging:
            print(f"DEBUG: Response status {response.status_code} for {endpoint_type}")
            print(f"DEBUG: Data received: {response.json()}") 
            
            response.raise_for_status()
            data = response.json()
            
            if isinstance(data, list) and len(data) > 0:
                return data
            return []
        except Exception as e:
            print(f"Error fetching {endpoint_type} data: {e}")
            return []
    # ---------------------------------

    def get_pitcher_data(self):
        # This will now use the debugged helper above
        data = self._fetch_from_api("pitchers")
        return pd.DataFrame(data) if data else pd.DataFrame()

    def get_batter_data(self):
        # This will now use the debugged helper above
        data = self._fetch_from_api("batters")
        return pd.DataFrame(data) if data else pd.DataFrame()
