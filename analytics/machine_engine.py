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
            # This print is critical—check your logs for this
            print(f"DEBUG: Params {params} returned keys: {list(data.keys())}", flush=True)
            return data
        except Exception as e:
            print(f"DEBUG: API Error: {e}", flush=True)
            return None

    def get_pitcher_data(self):
        # Broadened parameters to ensure we get a response
        params = {"sportId": 1, "group": "pitching", "type": "season", "sortStat": "era", "season": 2025}
        data = self._fetch_from_api("stats", params=params)
        return self._process_data(data)

    def get_batter_data(self):
        # Broadened parameters to ensure we get a response
        params = {"sportId": 1, "group": "hitting", "type": "season", "sortStat": "homeRuns", "season": 2025}
        data = self._fetch_from_api("stats", params=params)
        return self._process_data(data)

    def _process_data(self, data):
        # Check if the API returned a list or a nested dictionary
        if not data or 'stats' not in data:
            return pd.DataFrame()
        
        # Adjusting to the structure of the /stats endpoint
        stats = data['stats'][0].get('splits', [])
        if not stats:
            return pd.DataFrame()
            
        df = pd.json_normalize(stats)
        # Rename columns if they exist
        mapping = {'player.fullName': 'Player', 'stat.era': 'Value', 'stat.homeRuns': 'Value'}
        df = df.rename(columns=mapping)
        
        return df[['Player', 'Value']]
