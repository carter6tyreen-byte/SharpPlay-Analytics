    def run_starworld_optimizer(self, game_id):
        # 1. Fetch the data (replace with your actual API request logic)
        raw_data = self.fetch_roster_data(game_id) 
        all_players = []
        
        # 2. Iterate through the teams and their respective rosters
        for team in raw_data.get('teams', []):
            team_name = team.get('name', 'Unknown')
            team_side = team.get('side', 'N/A')
            
            # 3. Inner loop through each player on the roster
            for player in team.get('roster', []):
                # Map position using your helper method
                position_code = player.get('position', {}).get('abbreviation', 'N/A')
                full_position = self.get_position_name(position_code)
                
                # Append player details to our list
                all_players.append({
                    'Team': team_name,
                    'Side': team_side,
                    'Player': player.get('person', {}).get('fullName', 'Unknown'),
                    'Position': full_position,
                    'Status': player.get('status', {}).get('description', 'Active')
                })
        
        # 4. Return as a clean DataFrame
        return pd.DataFrame(all_players)
