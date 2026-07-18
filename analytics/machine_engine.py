import pandas as pd
import requests

class AnalyticsEngine:
    def __init__(self):
        self.base_url = "https://statsapi.mlb.com/api/v1"

    def _fetch_from_api(self, endpoint_type, params=None):
        try:
            url = f"{self.base_url}/{endpoint_type}"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            # This will appear in your Streamlit 'Manage app > See logs'
            print(f"DEBUG: API returned data for {params.get('season')}: {'leagueLeaders' in data}")
            return data
        except Exception as e:
            print(f"DEBUG: API Error: {e}")
            return None

    def get_pitcher_data(self):
        # Try 2026 first, then fallback to 2025
        for year in [2026, 2025]:
            params = {"sportId": 1, "statGroup": "pitching", "statType": "season", "leaderCategories": "era", "season": year}
            data = self._fetch_from_api("stats/leaders", params=params)
            
            if data and data.get('leagueLeaders'):
                return self._process_data(data)
        
        return pd.DataFrame() # Returns empty if both fail

    def get_batter_data(self):
        # Try 2026 first, then fallback to 2025
        for year in [2026, 2025]:
            params = {"sportId": 1, "statGroup": "hitting", "statType": "season", "leaderCategories": "homeRuns", "season": year}
            data = self._fetch_from_api("stats/leaders", params=params)
            
            if data and data.get('leagueLeaders'):
                return self._process_data(data)
        
        return pd.DataFrame()

    def _process_data(self, data):
        if not data or 'leagueLeaders' not in data:
            return pd.DataFrame()
        
        # Flatten the nested structure
        df = pd.json_normalize(data['leagueLeaders'])
        
        # Select and rename columns if they exist
        cols = {'person.fullName': 'Player', 'value': 'Value', 'rank': 'Rank'}
        df = df.rename(columns=cols)
        
        # Return only desired columns if present
        return df[[c for c in ['Rank', 'Player', 'Value'] if c in df.columns]]
