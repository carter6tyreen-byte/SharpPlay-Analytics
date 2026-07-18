import pandas as pd
import requests

class AnalyticsEngine:
    def __init__(self):
        self.base_url = "https://statsapi.mlb.com/api/v1"

    def _fetch_from_api(self, endpoint_type, params=None):
        url = f"{self.base_url}/{endpoint_type}"
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API Error: {e}")
            return None

    def _process_data(self, data):
        if not data or 'leagueLeaders' not in data:
            return pd.DataFrame()
        df = pd.json_normalize(data['leagueLeaders'])
        cols = {'person.fullName': 'Player', 'value': 'Value', 'rank': 'Rank'}
        df = df.rename(columns=cols)
        return df[[c for c in ['Rank', 'Player', 'Value'] if c in df.columns]]

    def get_pitcher_data(self):
        params = {"sportId": 1, "statGroup": "pitching", "statType": "season", "leaderCategories": "era", "season": 2025}
        data = self._fetch_from_api("stats/leaders", params=params)
        return self._process_data(data)

    def get_batter_data(self):
        params = {"sportId": 1, "statGroup": "hitting", "statType": "season", "leaderCategories": "homeRuns", "season": 2025}
        data = self._fetch_from_api("stats/leaders", params=params)
        return self._process_data(data)
