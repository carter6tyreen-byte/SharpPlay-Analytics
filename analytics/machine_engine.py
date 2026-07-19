import pandas as pd
import requests

class AnalyticsEngine:
    def __init__(self):
        self.base_url = "https://statsapi.mlb.com/api/v1"

    def _fetch_from_api(self, endpoint, params):
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API Error: {e}", flush=True)
            return None

    def _get_data(self, stat_group, category):
        # We use the 'stats' endpoint with 'type=season' to get the full list
        params = {
            "sportId": 1,
            "group": stat_group,
            "type": "season",
            "sortStat": category,
            "season": 2025,
            "limit": 10
        }
        data = self._fetch_from_api("stats", params=params)
        
        if not data or 'stats' not in data or not data['stats']:
            return pd.DataFrame()
            
        # The /stats endpoint returns data in the 'splits' list
        splits = data['stats'][0].get('splits', [])
        df = pd.json_normalize(splits)
        
        # Mapping to clean up common output names
        # Note: adjust these based on the actual columns found in your logs
        return df

    def get_pitcher_data(self):
        # Sorting by ERA usually requires the 'qualified' parameter or specific ranking
        return self._get_data("pitching", "era")

    def get_batter_data(self):
        return self._get_data("hitting", "homeRuns")
