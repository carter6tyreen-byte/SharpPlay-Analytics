import pandas as pd
import requests

class AnalyticsEngine:
    def __init__(self):
        self.base_url = "https://statsapi.mlb.com/api/v1"
        self.headers = {} 

    def _fetch_from_api(self, endpoint_type, params=None):
        """Fetches data from the MLB public API with optional parameters."""
        try:
            url = f"{self.base_url}/{endpoint_type}"
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            
            print(f"DEBUG: Response status {response.status_code} for {endpoint_type}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching {endpoint_type}: {e}")
            return None

    def get_pitcher_data(self):
        """Fetches pitching leaders."""
        # Example: Fetching ERA leaders for the 2026 season
        params = {"sportId": 1, "statGroup": "pitching", "statType": "season", "leaderCategories": "era", "season": 2026}
        data = self._fetch_from_api("stats/leaders", params=params)
        return self._process_data(data)

    def get_batter_data(self):
        """Fetches batting leaders."""
        # Example: Fetching Home Run leaders for the 2026 season
        params = {"sportId": 1, "statGroup": "hitting", "statType": "season", "leaderCategories": "homeRuns", "season": 2026}
        data = self._fetch_from_api("stats/leaders", params=params)
        return self._process_data(data)

    def _process_data(self, data):
        """Converts MLB JSON response into a clean DataFrame."""
        if not data or 'leagueLeaders' not in data:
            return pd.DataFrame()
        
        # MLB stats usually nest data under 'leagueLeaders'
        return pd.DataFrame(data['leagueLeaders'])
