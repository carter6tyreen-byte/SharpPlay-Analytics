import pandas as pd
import requests

class AnalyticsEngine:
    def __init__(self):
        self.base_url = "https://statsapi.mlb.com/api/v1"

    def _fetch_from_api(self, endpoint, params):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API Error: {e}", flush=True)
            return None

    def _get_stats(self, stat_group, sort_stat, order="desc"):
        params = {
            "sportId": 1, 
            "group": stat_group, 
            "stats": "season",
            "season": 2026,
            "order": order,
            "sortStat": sort_stat,
            "limit": 100
        }
        data = self._fetch_from_api("stats", params=params)
        
        if not data or 'stats' not in data or not data['stats']:
            return pd.DataFrame()
            
        splits = data['stats'][0].get('splits', [])
        df = pd.json_normalize(splits)
        
        # Filter: Only include players with roster status 'A' (Active)
        status_field = 'status_code' if 'status_code' in df.columns else 'player.status.code'
        if status_field in df.columns:
            df = df[df[status_field] == 'A']
        
        rename_map = {
            'player.fullName': 'Player', 
            'team.name': 'Team', 
            f'stat.{sort_stat}': 'Value'
        }
        
        df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
        
        required_cols = ['Player', 'Team', 'Value']
        if all(col in df.columns for col in required_cols):
            return df[required_cols].head(10)
        return pd.DataFrame()

    def get_pitcher_data(self):
        # Sort ERA ascending: Lowest (best) ERA at the top
        return self._get_stats("pitching", "era", order="asc")

    def get_batter_data(self):
        # Sort HR descending: Highest (best) HR at the top
        return self._get_stats("hitting", "homeRuns", order="desc")
