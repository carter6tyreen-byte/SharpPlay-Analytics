    def _process_data(self, data):
        """Converts MLB JSON response into a clean DataFrame by normalizing nested objects."""
        if not data or 'leagueLeaders' not in data:
            return pd.DataFrame()
        
        # 1. Normalize the 'leagueLeaders' list
        # This automatically flattens dictionaries like 'person' and 'stat'
        df = pd.json_normalize(data['leagueLeaders'])
        
        # 2. Clean up column names for readability
        # json_normalize creates names like 'person.fullName' and 'stat'
        df = df.rename(columns={
            'person.fullName': 'Player',
            'stat': 'Value',
            'rank': 'Rank'
        })
        
        # 3. Drop unnecessary columns if you only want the basics
        # Keep only what you actually need to see in the table
        cols_to_keep = ['Rank', 'Player', 'Value']
        # Add 'team.name' if you want to see the team
        if 'team.name' in df.columns:
            cols_to_keep.append('team.name')
            
        return df[cols_to_keep]
import pandas as pd
import requests

class AnalyticsEngine:
    def __init__(self):
        self.base_url = "https://statsapi.mlb.com/api/v1"
        self.headers = {} 

    # ... (Keep your _fetch_from_api, get_pitcher_data, and get_batter_data methods) ...

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
