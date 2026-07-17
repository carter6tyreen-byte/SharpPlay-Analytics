def run_starworld_optimizer(self, player_name):
    # 1. Fetch all games/rosters first to find the player
    # (Assuming you have a method like get_all_games)
    all_games_data = self.get_all_games() 
    
    # 2. Iterate to find the game_id where the player is playing
    target_game_id = None
    for game in all_games_data.get('games', []):
        # This logic depends on how your API structure looks
        # You need to check if 'player_name' exists in the roster of this game
        roster_data = self.fetch_roster_data(game['gamePk'])
        
        # Search for the player in this game's roster
        for team in roster_data.get('teams', []):
            for player in team.get('roster', []):
                if player.get('person', {}).get('fullName') == player_name:
                    target_game_id = game['gamePk']
                    break
        if target_game_id:
            break
    
    # 3. If found, run your established logic
    if target_game_id:
        return self.run_starworld_optimizer_by_id(target_game_id)
    else:
        print(f"Player {player_name} not found in active games.")
        return pd.DataFrame() # Return empty if not found

# Rename your functional code to this
def run_starworld_optimizer_by_id(self, game_id):
    # This is your existing code that works with a game_id
    raw_data = self.fetch_roster_data(game_id)
    # ... rest of your original logic ...
