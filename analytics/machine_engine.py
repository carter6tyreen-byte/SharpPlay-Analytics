    def get_all_games(self):
        """Returns all games from all dates in the schedule."""
        all_games = []
        # The new structure nests games inside 'dates'
        for date_entry in self.matchup_data.get('dates', []):
            for game in date_entry.get('games', []):
                # Safely get team names
                away = game.get('teams', {}).get('away', {}).get('team', {}).get('name', 'Unknown')
                home = game.get('teams', {}).get('home', {}).get('team', {}).get('name', 'Unknown')
                
                all_games.append({
                    'GameID': game.get('gamePk'),
                    'Game': f"{away} vs {home}"
                })
        return pd.DataFrame(all_games)
