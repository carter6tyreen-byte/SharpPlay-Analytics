    def _process_data(self, data):
        """Converts MLB JSON response into a clean DataFrame and flattens nested dicts."""
        if not data or 'leagueLeaders' not in data:
            return pd.DataFrame()
        
        # 1. Create the DataFrame
        df = pd.DataFrame(data['leagueLeaders'])
        
        # 2. Flatten dictionary columns (e.g., gameType -> gameType['description'])
        for col in df.columns:
            # Check if the first cell of the column is a dict
            if isinstance(df[col].iloc[0], dict):
                # Extract the 'description' or 'name' if available
                if 'description' in df[col].iloc[0]:
                    df[col] = df[col].apply(lambda x: x.get('description') if isinstance(x, dict) else x)
                elif 'name' in df[col].iloc[0]:
                    df[col] = df[col].apply(lambda x: x.get('name') if isinstance(x, dict) else x)
                    
        return df
