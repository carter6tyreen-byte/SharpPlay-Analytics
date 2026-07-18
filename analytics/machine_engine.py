import pandas as pd
import requests

class AnalyticsEngine:
    def __init__(self):
        self.base_url = "https://statsapi.mlb.com/api/v1"

    def _fetch_from_api(self, endpoint_type, params=None):
        url = f"{self.base_url}/{endpoint_type}"
        try:
            # Add print here to confirm the exact URL being called
            print(f"DEBUG: Calling URL: {url} with params {params}", flush=True)
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Print the first 100 chars of the data to verify what the API actually returned
            print(f"DEBUG: Data snippet: {str(data)[:100]}", flush=True)
            return data
        except Exception as e:
            print(f"DEBUG: CRITICAL API ERROR: {e}", flush=True)
            return None

    def get_pitcher_data(self):
        # We only check 2025 for now to verify data connectivity
        params = {"sportId": 1, "statGroup": "pitching", "statType": "season", "leaderCategories": "era", "season": 2025}
        data = self._fetch_from_api("stats/leaders", params=params)
        
        if data and 'leagueLeaders' in data and len(data['leagueLeaders']) > 0:
            return self._process_data(data)
        else:
            print("DEBUG: No leagueLeaders found in response for 2025", flush=True)
            return None
