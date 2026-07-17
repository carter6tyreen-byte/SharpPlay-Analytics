import pandas as pd
import json
import streamlit as st

# 1. Move this to a standalone function so it can be cached easily
@st.cache_data(ttl=3600)
def load_matchup_data():
    try:
        with open('data/today_matchups.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"dates": []}

class AnalyticsEngine:
    def __init__(self):
        # The class no longer needs to store matchup_data as an instance variable
        pass

    def get_all_games(self):
        # 2. Call the standalone function instead of using self
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
