import streamlit as st
import pandas as pd
import json
import os

# Configuration
LOG_FILE = 'predictions_log.csv'
MATCHUP_FILE = 'data/today_matchups.json'

def load_matchup_data():
    """Parses JSON to extract game metadata and lists of players for dropdowns."""
    if not os.path.exists(MATCHUP_FILE):
        return []
    
    with open(MATCHUP_FILE, 'r') as f:
        data = json.load(f)
        all_games = []
        for entry in data.get('dates', []):
            for game in entry.get('games', []):
                # Logic: Extract team names, and identify pitcher/hitter lists
                # Note: Adjust these keys if your JSON structure differs slightly
                flat_game = {
                    'gamePk': game.get('gamePk'),
                    'away_team': game.get('teams', {}).get('away', {}).get('team', {}).get('name'),
                    'home_team': game.get('teams', {}).get('home', {}).get('team', {}).get('name'),
                    'pitchers': ['TBD'], # Placeholder: Populate based on your JSON structure
                    'hitters': ['Player 1', 'Player 2'] # Placeholder: Populate based on your JSON structure
                }
                all_games.append(flat_game)
        return all_games

def initialize_log():
    if not os.path.exists(LOG_FILE):
        df = pd.DataFrame(columns=['timestamp', 'game_id', 'matchup', 'pitcher', 'hitter', 'pred_hr', 'actual_hr', 'status'])
        df.to_csv(LOG_FILE, index=False)

st.set_page_config(page_title="ProAnalytics Dashboard", layout="wide")
st.title("⚾ ProAnalytics Performance Tracker")
initialize_log()

# 1. Display Matchups
matchups = load_matchup_data()
if matchups:
    df_matchups = pd.DataFrame(matchups).drop(columns=['pitchers', 'hitters'], errors='ignore')
    st.dataframe(df_matchups, width='stretch')

# 2. Dynamic Input Form
st.subheader("Add New Prediction")
with st.form("prediction_form"):
    game_options = {f"{g['away_team']} vs {g['home_team']}": g for g in matchups}
    selected_name = st.selectbox("Select Matchup", list(game_options.keys()))
    selected_data = game_options[selected_name]
    
    # Scrollable selects instead of text input
    pitcher = st.selectbox("Starting Pitcher", selected_data.get('pitchers', []))
    hitter = st.selectbox("Hitter", selected_data.get('hitters', []))
    pred_hr = st.number_input("Predicted HRs", min_value=0, step=1)
    
    if st.form_submit_button("Log Prediction"):
        new_entry = pd.DataFrame([{
            'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M'),
            'game_id': selected_data['gamePk'],
            'matchup': selected_name,
            'pitcher': pitcher,
            'hitter': hitter,
            'pred_hr': pred_hr,
            'actual_hr': 0,
            'status': 'Pending'
        }])
        new_entry.to_csv(LOG_FILE, mode='a', header=False, index=False)
        st.success(f"Logged {hitter} vs {pitcher}!")
        st.rerun()

# 3. Results
st.subheader("Prediction vs. Actual Results")
if os.path.exists(LOG_FILE):
    st.dataframe(pd.read_csv(LOG_FILE), width='stretch')
