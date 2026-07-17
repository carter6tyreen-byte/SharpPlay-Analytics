import pandas as pd
import json
import streamlit as st

class AnalyticsEngine:
    def __init__(self):
        pass

    @st.cache_data(ttl=3600)  # Refreshes data every hour (3600 seconds)
    def load_matchup_data(self):
        try:
            with open('data/today_matchups.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"dates": []}

    def get_all_games(self):
        matchup_data = self.load_matchup_data()
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
