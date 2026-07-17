    def run_starworld_optimizer(self, player_name):
        games_data = self.get_all_games()
        games = games_data.get('games', [])
        
        # DEBUG: Print the number of games found
        print(f"DEBUG: Found {len(games)} games to scan.")

        for game in games:
            game_id = game.get('gamePk')
            roster_data = self.fetch_roster_data(game_id)
            
            # DEBUG: See if roster data is actually returned
            if not roster_data:
                continue
                
            teams = roster_data.get('teams', {})
            for side in ['away', 'home']:
                team_info = teams.get(side, {})
                roster = team_info.get('roster', {}).get('roster', [])
                
                for player in roster:
                    name = player.get('person', {}).get('fullName')
                    # DEBUG: Print names found to check for spelling mismatches
                    if name:
                        print(f"DEBUG: Checking {name} against {player_name}")
                    
                    if name == player_name:
                        return pd.DataFrame(...)
        
        print("DEBUG: Player not found after scanning all rosters.")
        return pd.DataFrame()
