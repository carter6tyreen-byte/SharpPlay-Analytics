    def _process_data(self, data):
        """Converts MLB JSON response into a clean DataFrame with safety checks."""
        # Check if data exists and contains 'leagueLeaders'
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
            
        # Filter: only keep columns that are actually present
        existing_cols = [c for c in required_cols if c in df.columns]
        
        # If no columns match, return empty to prevent crash
        if not existing_cols:
            return pd.DataFrame()
            
        return df[existing_cols]
