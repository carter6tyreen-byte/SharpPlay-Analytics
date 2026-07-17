import pandas as pd
import json
import requests
import streamlit as st

@st.cache_data(ttl=3600)
def load_matchup_data():
    try:
        with open('data/today_matchups.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"dates": []}

class AnalyticsEngine:
    def __init__(self):
        pass

    def get_all_games(self):
        matchup_data = load_matchup_data()
        all_games = []
        for date_entry in matchup_data.get('dates', []):
            for game in date_entry.get('games', []):
                away = game.get('teams', {}).get('away', {}).get('team', {}).get('name', 'Unknown')
                home = game.get('teams', {}).get('home', {}).get('team', {}).get('name', 'Unknown')
                all_games.append({
                    'GameID': game.get('gamePk'),
                    'Game': f"{away} at {home}"
                })
        return pd.DataFrame(all_games)

    def run_starworld_optimizer(self, game_id):
        # Call the standalone function here as well
        matchup_data = load_matchup_data()
        target_game = None
        for date_entry in matchup_data.get('dates', []):
            for game in date_entry.get('games', []):
                if str(game.get('gamePk')) == str(game_id):
                    target_game = game
                    break
        
        if not target_game:
            return pd.DataFrame([{"Error": "Game ID not found"}])

        all_players = []
        teams_to_fetch = [
            {'id': target_game['teams']['away']['team']['id'], 'name': target_game['teams']['away']['team']['name'], 'side': 'Away'},
            {'id': target_game['teams']['home']['team']['id'], 'name': target_game['teams']['home']['team']['name'], 'side': 'Home'}
        ]
        
        for t in teams_to_fetch:
            try:
                url = f"https://statsapi.mlb.com/api/v1/teams/{t['id']}/roster"
                response = requests.get(url, timeout=10).json()
                for p in response.get('roster', []):
                    all_players.append({
                        'Team': t['name'],
                        'Side': t['side'],
                        'Player': p.get('person', {}).get('fullName', 'Unknown'),
                        'Position': p.get('position', {}).get('abbreviation', 'N/A'),
                        'Status': p.get('status', {}).get('description', 'Active')
                    })
            except Exception:
                continue
            
        return pd.DataFrame(all_players) if all_players else pd.DataFrame([{"Message": "Roster data unavailable"}])
