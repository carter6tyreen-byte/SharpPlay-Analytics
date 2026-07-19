    def _get_stats(self, stat_group, sort_stat):
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
        
        # We add 'team.name' and 'opponent.name' if available in the API response
        rename_map = {
            'player.fullName': 'Player', 
            f'stat.{sort_stat}': 'Value',
            'team.name': 'Team' 
        }
        
        df = df.rename(columns=rename_map)
        # Select relevant columns
        cols = ['Player', 'Team', 'Value']
        return df[cols] if all(c in df.columns for c in cols) else pd.DataFrame()
