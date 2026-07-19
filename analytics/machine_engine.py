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

    def _get_stats(self, group, sort_stat):
        # Using the standard stats endpoint with required parameters
        params = {
            "sportId": 1,
            "group": group,
            "type": "season",
            "sortStat": sort_stat,
            "season": 2025,
            "limit": 10
        }
        data = self._fetch_from_api("stats", params=params)
        
        if not data or 'stats' not in data or len(data['stats']) == 0:
            return pd.DataFrame()
            
        # Extract data from the 'splits' list
        splits = data['stats'][0].get('splits', [])
        if not splits:
            return pd.DataFrame()
            
        df = pd.json_normalize(splits)
        
        # Mapping API fields to readable table headers
        # 'player.fullName' is standard for both pitching and hitting
        rename_map = {
            'player.fullName': 'Player', 
            'stat.' + sort_stat: 'Value'
        }
        
        # Filter and rename
        df = df.rename(columns=rename_map)
        if 'Player' in df.columns and 'Value' in df.columns:
            return df[['Player', 'Value']]
        return pd.DataFrame()

    def get_pitcher_data(self):
        return self._get_stats("pitching", "era")

    def get_batter_data(self):
        return self._get_stats("hitting", "homeRuns")
