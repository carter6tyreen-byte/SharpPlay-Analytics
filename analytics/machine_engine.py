import pandas as pd

class AnalyticsEngine:
    def __init__(self):
        # Initialize your API/data connections here
        pass

    def get_all_games(self):
        # Ensure this returns a DataFrame or list of game objects
        # You may need to verify this matches your existing API logic
        return self.fetch_schedule_from_api()

    def run_starworld_optimizer(self, player_name):
        # 1. Fetch current games
        games_data = self.get_all_games()
        games = games_data.get('games', [])
        
        # 2. Iterate to locate the player across all active games
        for game in games:
            game_id = game.get('gamePk')
            roster_data = self.fetch_roster_data(game_id)
            
            # 3. Check both Away and Home teams
            for team_key in ['away', 'home']:
                team = roster_data.get('teams', {}).get(team_key, {})
                roster = team.get('roster', {}).get('roster', [])
                
                for player in roster:
                    if player.get('person', {}).get('fullName') == player_name:
                        # 4. Return the specific player's data as a DataFrame
                        return pd.DataFrame([{
                            'Player': player_name,
                            'Team': team.get('team', {}).get('name'),
                            'Position': player.get('position', {}).get('abbreviation'),
                            'Status': player.get('status', {}).get('description'),
                            'GameID': game_id
                        }])
        
        # 5. Return empty if player is not found
        return pd.DataFrame()

    def fetch_roster_data(self, game_id):
        # Your existing API logic to fetch roster by game ID
        # return data_from_mlb_api(game_id)
        pass

    def fetch_schedule_from_api(self):
        # Your existing API logic to fetch the daily schedule
        # return data_from_mlb_api()
        pass
