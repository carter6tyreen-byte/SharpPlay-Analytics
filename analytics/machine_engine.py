import pandas as pd
import requests

class AnalyticsEngine:
    def __init__(self):
        self.base_url = "https://statsapi.mlb.com/api/v1"

    def _fetch_from_api(self, endpoint, params):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(f"{self.base_url}/{endpoint}", params=params, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API Error: {e}", flush=True)
            return None

    def _get_stats(self, stat_group, sort_stat):
        params = {
            "sportId": 1, "group": stat_group, "stats": "season",
            "season": 2025, "order": "desc", "sortStat": sort_stat, "limit": 10
        }
        data = self._fetch_from_api("stats", params=params)
        
        if not data or 'stats' not in data or not data['stats']:
            return pd.DataFrame()
            
        df = pd.json_normalize(data['stats'][0].get('splits', []))
        
        # Mapping API fields: 'team.name' provides context
        rename_map = {
            'player.fullName': 'Player', 
            'team.name': 'Team',
            f'stat.{sort_stat}': 'Value'
        }
        df = df.rename(columns=rename_map)
        
        # Return necessary columns for the board
        cols = ['Player', 'Team', 'Value']
        return df[cols] if all(c in df.columns for c in cols) else pd.DataFrame()

    def get_pitcher_data(self):
        return self._get_stats("pitching", "era")

    def get_batter_data(self):
        return self._get_stats("hitting", "homeRuns")
