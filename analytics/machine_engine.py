import pandas as pd

class AnalyticsEngine:
    def __init__(self):
        pass

    def get_all_games(self):
        # Fetch data and default to an empty structure if API returns None
        data = self.fetch_schedule_from_api()
        if data is None:
            return {'games': []}
        return data

    def run_starworld_optimizer(self, player_name):
        # 1. Fetch current games using the safe method
        games_data = self.get_all_games()
        games = games_data.get('games', [])
        
        # 2. Iterate to locate the player across all active games
        for game in games:
            game_id = game.get('gamePk')
            if not game_id:
                continue
                
            roster_data = self.fetch_roster_data(game_id)
            if not roster_data:
                continue
            
            # 3. Check both Away and Home teams
            teams = roster_data.get('teams', {})
            for side in ['away', 'home']:
                team_info = teams.get(side, {})
                roster = team_info.get('roster', {}).get('roster', [])
                
                for player in roster:
                    if player.get('person', {}).get('fullName') == player_name:
                        # 4. Return the specific player's data as a DataFrame
                        return pd.DataFrame([{
                            'Player': player_name,
                            'Team': team_info.get('team', {}).get('name', 'N/A'),
                            'Position': player.get('position', {}).get('abbreviation', 'N/A'),
                            'Status': player.get('status', {}).get('description', 'N/A'),
                            'GameID': game_id
                        }])
        
        # 5. Return empty DataFrame if player is not found or API data is missing
        return pd.DataFrame()

    def fetch_roster_data(self, game_id):
        # Ensure this method handles failures gracefully by returning {} or None
        pass

    def fetch_schedule_from_api(self):
        # Ensure this method handles failures gracefully by returning {} or None
        pass
