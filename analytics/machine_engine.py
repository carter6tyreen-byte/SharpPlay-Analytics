import pandas as pd
import requests

class AnalyticsEngine:
    def __init__(self):
        self.base_url = "https://statsapi.mlb.com/api/v1"

    def _fetch_from_api(self, endpoint, params):
        url = f"{self.base_url}/{endpoint}"
        try:
            # Using headers to ensure the request is identified correctly
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API Error: {e}", flush=True)
            return None

    def _get_stats(self, stat_group, sort_stat):
        # Updated parameters to avoid the 400 Bad Request error
        params = {
            "sportId": 1,
            "group": stat_group,
            "stats": "season",
            "season": 2025,
            "order": "desc",
            "sortStat": sort_stat,
            "limit": 10
        }
        data = self._fetch_from_api("stats", params=params)
        
        if not data or 'stats' not in data or not data['stats']:
            return pd.DataFrame()
            
        splits = data['stats'][0].get('splits', [])
        df = pd.json_normalize(splits)
        
        # Mapping column names based on API response structure
        rename_map = {'player.fullName': 'Player', f'stat.{sort_stat}': 'Value'}
        df = df.rename(columns=rename_map)
        
        return df[['Player', 'Value']] if 'Player' in df.columns else pd.DataFrame()

    def get_pitcher_data(self):
        return self._get_stats("pitching", "era")

    def get_batter_data(self):
        return self._get_stats("hitting", "homeRuns")
