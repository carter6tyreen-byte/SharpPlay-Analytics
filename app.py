import streamlit as st
import pandas as pd
import json
import os

LOG_FILE = 'predictions_log.csv'
MATCHUP_FILE = 'data/today_matchups.json'

def load_matchup_data():
    """Parses JSON for matchups, statuses, and available player names."""
    if not os.path.exists(MATCHUP_FILE):
        return []
    
    with open(MATCHUP_FILE, 'r') as f:
        try:
            data = json.load(f)
            games_list = []
            for entry in data.get('dates', []):
                game_date = entry.get('date')
                for game in entry.get('games', []):
                    teams = game.get('teams', {})
                    home = teams.get('home', {})
                    away = teams.get('away', {})
                    
                    # Extract hydrated lineup data
                    h_hitters = [p.get('fullName') for p in home.get('lineup', [])]
                    a_hitters = [p.get('fullName') for p in away.get('lineup', [])]
                    
                    games_list.append({
                        'date': game_date,
                        'gamePk': game.get('gamePk'),
                        'matchup': f"{away.get('team',{}).get('name')} vs {home.get('team',{}).get('name')}",
                        'status': game.get('status', {}).get('detailedState', 'Scheduled'),
                        'hitters': (h_hitters + a_hitters) or ['Lineup pending'],
                        'home_team': home.get('team', {}).get('name'),
                        'away_team': away.get('team', {}).get('name')
                    })
            return games_list
        except:
            return []

# --- App UI ---
st.set_page_config(page_title="ProAnalytics", layout="wide")
st.title("⚾ ProAnalytics Performance Tracker")

matchups = load_matchup_data()

if matchups:
    df = pd.DataFrame(matchups)
    
    # 1. Dashboard Table
    st.subheader("Upcoming Slate (Today & Tomorrow)")
    display_df = df[['date', 'matchup', 'status']]
    st.dataframe(display_df, use_container_width=True)

    # 2. Prediction Form
    st.subheader("Add New Prediction")
    with st.form("pred_form"):
        # Only allow active/scheduled games
        active_games = [m for m in matchups if m['status'] != 'Postponed']
        selected_matchup = st.selectbox("Select Matchup", [f"{m['date']} | {m['matchup']}" for m in active_games])
        
        # Extract selected game object
        game_obj = next(m for m in active_games if f"{m['date']} | {m['matchup']}" == selected_matchup)
        
        hitter = st.selectbox("Select Hitter", game_obj['hitters'])
        pred_hr = st.number_input("Predicted HRs", min_value=0, step=1)
        
        if st.form_submit_button("Log Prediction"):
            if hitter == 'Lineup pending':
                st.error("Cannot log prediction: Lineup not yet available.")
            else:
                new_entry = pd.DataFrame([{
                    'date': game_obj['date'],
                    'matchup': game_obj['matchup'],
                    'hitter': hitter,
                    'pred_hr': pred_hr
                }])
                # Save locally
                new_entry.to_csv(LOG_FILE, mode='a', header=not os.path.exists(LOG_FILE), index=False)
                st.success(f"Prediction logged for {hitter}!")
else:
    st.warning("No data found in `data/today_matchups.json`. Run your collector script first.")
