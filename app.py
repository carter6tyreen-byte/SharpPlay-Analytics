import pandas as pd
import requests

class AnalyticsEngine:
    def __init__(self):
        self.base_url = "https://statsapi.mlb.com/api/v1"
        self.headers = {} 

    def _fetch_from_api(self, endpoint_type, params=None):
        try:
            url = f"{self.base_url}/{endpoint_type}"
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching {endpoint_type}: {e}")
            return None

    def get_pitcher_data(self):
        params = {"sportId": 1, "statGroup": "pitching", "statType": "season", "leaderCategories": "era", "season": 2026}
        data = self._fetch_from_api("stats/leaders", params=params)
        return self._process_data(data)

    def get_batter_data(self):
        params = {"sportId": 1, "statGroup": "hitting", "statType": "season", "leaderCategories": "homeRuns", "season": 2026}
        data = self._fetch_from_api("stats/leaders", params=params)
        return self._process_data(data)

    def _process_data(self, data):
        """Converts MLB JSON response into a clean DataFrame with safety checks."""
        if not data or 'leagueLeaders' not in data or not data['leagueLeaders']:
            return pd.DataFrame()
        
        # 1. Normalize the 'leagueLeaders' list
        df = pd.json_normalize(data['leagueLeaders'])
        
        # 2. Rename columns only if they exist in the DataFrame
        rename_map = {
            'person.fullName': 'Player',
            'stat': 'Value',
            'rank': 'Rank'
        }
        df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
        
        # 3. Safely select only columns that exist
        required_cols = ['Rank', 'Player', 'Value']
        if 'team.name' in df.columns:
            required_cols.append('team.name')
            
        existing_cols = [c for c in required_cols if c in df.columns]
        
        if not existing_cols:
            return pd.DataFrame()
            
        return df[existing_cols]
