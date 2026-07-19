import streamlit as st
import pandas as pd
import json
import os

# Configuration
LOG_FILE = 'predictions_log.csv'
MATCHUP_FILE = 'data/today_matchups.json'

def load_matchup_data():
    """Parses JSON to extract game metadata, status, and player lists."""
    if not os.path.exists(MATCHUP_FILE):
        return []
    
    with open(MATCHUP_FILE, 'r') as f:
        try:
            data = json.load(f)
            all_games = []
            for entry in data.get('dates', []):
                for game in entry.get('games', []):
                    # Extract game details and status
                    status_info = game.get('status', {})
                    
                    # Placeholder lists: In the next step, update these to parse your JSON paths
                    # e.g., game.get('lineups', {}).get('homePlayers', [])
                    flat_game = {
                        'gamePk': game.get('gamePk'),
                        'away_team': game.get('teams', {}).get('away', {}).get('team', {}).get('name'),
                        'home_team': game.get('teams', {}).get('home', {}).get('team', {}).get('name'),
                        'status': status_info.get('detailedState', 'Unknown'),
                        'pitchers': ['Pitcher A', 'Pitcher B'], 
                        'hitters': ['Hitter A', 'Hitter B']
                    }
                    all_games.append(flat_game)
            return all_games
        except json.JSONDecodeError:
            return []

def initialize_log():
    if not os.path.exists(LOG_FILE):
        df = pd.DataFrame(columns=['timestamp', 'game_id', 'matchup', 'pitcher', 'hitter', 'pred_hr', 'actual_hr', 'status'])
        df.to_csv(LOG_FILE, index=False)

st.set_page_config(page_title="ProAnalytics Dashboard", layout="wide")
st.title("⚾ ProAnalytics Performance Tracker")
initialize_log()

# 1. Display Matchups (Filtering out Postponed)
matchups = load_matchup_data()
if matchups:
    df_matchups = pd.DataFrame(matchups)
    # Only show active/scheduled games
    active_games = df_matchups[df_matchups['status'] != 'Postponed']
    
    st.subheader("Today's Active Matchups")
    st.dataframe(active_games.drop(columns=['pitchers', 'hitters'], errors='ignore'), width='stretch')
else:
    st.info("No matchup data found or all games postponed.")

# 2. Dynamic Input Form
if matchups:
    st.subheader("Add New Prediction")
    with st.form("prediction_form"):
        # Filter active games for the dropdown
        active_matchups = [g for g in matchups if g['status'] != 'Postponed']
        game_options = {f"{g['away_team']} vs {g['home_team']}": g for g in active_matchups}
        
        selected_name = st.selectbox("Select Matchup", list(game_options.keys()))
        selected_data = game_options[selected_name]
        
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
