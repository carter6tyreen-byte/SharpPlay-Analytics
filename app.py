import streamlit as st
import pandas as pd
import json
import os

# Configuration
LOG_FILE = 'predictions_log.csv'
MATCHUP_FILE = 'data/today_matchups.json'
# Add your frequent hitters here
FREQUENT_HITTERS = ["Shohei Ohtani", "Aaron Judge", "Juan Soto", "Bryce Harper", "Mookie Betts"]

def load_matchup_data():
    """Loads JSON data and flattens nested structures."""
    if os.path.exists(MATCHUP_FILE):
        with open(MATCHUP_FILE, 'r') as f:
            data = json.load(f)
            all_games = []
            for entry in data.get('dates', []):
                for game in entry.get('games', []):
                    flat_game = {
                        'gamePk': game.get('gamePk'),
                        'away_team': game.get('teams', {}).get('away', {}).get('team', {}).get('name'),
                        'home_team': game.get('teams', {}).get('home', {}).get('team', {}).get('name')
                    }
                    all_games.append(flat_game)
            return all_games
    return []

def initialize_log():
    """Ensure the log file exists."""
    if not os.path.exists(LOG_FILE):
        df = pd.DataFrame(columns=['timestamp', 'game_id', 'matchup', 'hitter', 'pred_hr', 'actual_hr', 'status'])
        df.to_csv(LOG_FILE, index=False)

# UI Display
st.set_page_config(page_title="ProAnalytics Dashboard", layout="wide")
st.title("⚾ ProAnalytics Performance Tracker")

initialize_log()

# 1. Display Today's Data (Hiding gamePk)
st.subheader("Today's Matchup Insights")
matchups = load_matchup_data()
if matchups:
    df_matchups = pd.DataFrame(matchups)
    # Display table without the gamePk column
    st.dataframe(df_matchups.drop(columns=['gamePk']), width='stretch')
else:
    st.info("No matchup data found. Please ensure data_collector.py has run.")

# 1.5 Prediction Input Form
st.subheader("Add New Prediction")
with st.form("prediction_form"):
    game_options = {f"{g['away_team']} vs {g['home_team']}": g['gamePk'] for g in matchups}
    selected_matchup = st.selectbox("Select Matchup", list(game_options.keys()))
    
    # Scrollable list for hitters
    hitter = st.selectbox("Select Hitter", options=FREQUENT_HITTERS)
    pred_hr = st.number_input("Predicted HRs", min_value=0, step=1)
    
    submitted = st.form_submit_button("Log Prediction")
    
    if submitted:
        new_entry = pd.DataFrame([{
            'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M'),
            'game_id': game_options[selected_matchup],
            'matchup': selected_matchup,
            'hitter': hitter,
            'pred_hr': pred_hr,
            'actual_hr': 0,
            'status': 'Pending'
        }])
        new_entry.to_csv(LOG_FILE, mode='a', header=False, index=False)
        st.success(f"Prediction logged for {hitter}!")
        st.rerun()

# 2. Performance Tracking
st.subheader("Prediction vs. Actual Results")
logs = pd.read_csv(LOG_FILE)

def color_status(val):
    color = 'green' if val == 'Finished' else 'orange'
    return f'background-color: {color}'

if not logs.empty:
    st.dataframe(
        logs.style.map(color_status, subset=['status']),
        width='stretch'
    )
    
    finished = logs[logs['status'] == 'Finished']
    if not finished.empty:
        acc = (finished['pred_hr'] == finished['actual_hr']).mean() * 100
        st.metric("Model Hit Rate", f"{acc:.1f}%")
else:
    st.write("No predictions logged yet.")
