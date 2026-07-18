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
            data = response.json()
            # Diagnostic: check if the 'leagueLeaders' key exists
            print(f"DEBUG: Data keys: {list(data.keys())}", flush=True)
            return data
        except Exception as e:
            print(f"API Error: {e}", flush=True)
            return None

    def get_pitcher_data(self):
        # Correct parameters for the leaders endpoint
        params = {
            "sportId": 1, 
            "statGroup": "pitching", 
            "statType": "season", 
            "leaderCategories": "era", 
            "season": 2025
        }
        data = self._fetch_from_api("stats/leaders", params=params)
        return self._process_data(data)

    def get_batter_data(self):
        # Correct parameters for the leaders endpoint
        params = {
            "sportId": 1, 
            "statGroup": "hitting", 
            "statType": "season", 
            "leaderCategories": "homeRuns", 
            "season": 2025
        }
        data = self._fetch_from_api("stats/leaders", params=params)
        return self._process_data(data)

    def _process_data(self, data):
        if not data or 'leagueLeaders' not in data:
            return pd.DataFrame()
        
        # Normalize the list of dicts
        df = pd.json_normalize(data['leagueLeaders'])
        
        # Select and rename columns if they exist
        rename_map = {'person.fullName': 'Player', 'value': 'Value', 'rank': 'Rank'}
        df = df.rename(columns=rename_map)
        
        # Return columns if they exist
        cols = [c for c in ['Rank', 'Player', 'Value'] if c in df.columns]
        return df[cols]
