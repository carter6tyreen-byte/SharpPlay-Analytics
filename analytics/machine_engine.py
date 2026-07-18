import pandas as pd
import requests

class AnalyticsEngine:
    def __init__(self):
        # Official MLB Stats API base URL
        self.base_url = "https://statsapi.mlb.com/api/v1"
        self.headers = {} 

    def _fetch_from_api(self, endpoint_type, params=None):
        """Fetches data from the MLB public API."""
        try:
            url = f"{self.base_url}/{endpoint_type}"
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching {endpoint_type}: {e}")
            return None

    def get_pitcher_data(self):
        """Fetches pitching leaders."""
        params = {"sportId": 1, "statGroup": "pitching", "statType": "season", "leaderCategories": "era", "season": 2026}
        data = self._fetch_from_api("stats/leaders", params=params)
        return self._process_data(data)

    def get_batter_data(self):
        """Fetches batting leaders."""
        params = {"sportId": 1, "statGroup": "hitting", "statType": "season", "leaderCategories": "homeRuns", "season": 2026}
        data = self._fetch_from_api("stats/leaders", params=params)
        return self._process_data(data)

    def _process_data(self, data):
        """Converts MLB JSON response into a clean DataFrame by normalizing nested objects."""
        if not data or 'leagueLeaders' not in data:
            return pd.DataFrame()
        
        # 1. Normalize the 'leagueLeaders' list
        df = pd.json_normalize(data['leagueLeaders'])
        
        # 2. Clean up column names for readability
        df = df.rename(columns={
            'person.fullName': 'Player',
            'stat': 'Value',
            'rank': 'Rank'
        })
        
        # 3. Keep only necessary columns
        cols_to_keep = ['Rank', 'Player', 'Value']
        if 'team.name' in df.columns:
            cols_to_keep.append('team.name')
            
        return df[cols_to_keep]
