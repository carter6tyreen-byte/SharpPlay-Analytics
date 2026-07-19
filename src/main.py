import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Configuration & Setup
LOG_FILE = 'predictions_log.csv'

def initialize_log():
    """Ensure the log file exists with proper headers."""
    if not os.path.exists(LOG_FILE):
        df = pd.DataFrame(columns=['timestamp', 'game_id', 'matchup', 'hitter', 'pred_hr', 'actual_hr', 'status'])
        df.to_csv(LOG_FILE, index=False)

def log_prediction(game_id, matchup, hitter, pred_hr):
    """Saves a new recommendation to the tracker."""
    new_data = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'game_id': game_id,
        'matchup': matchup,
        'hitter': hitter,
        'pred_hr': pred_hr,
        'actual_hr': 0, # Placeholder until game finishes
        'status': 'Pending'
    }
    df = pd.DataFrame([new_data])
    df.to_csv(LOG_FILE, mode='a', header=False, index=False)

def update_results(game_id, actual_hr):
    """Updates a pending prediction with real-world results."""
    df = pd.read_csv(LOG_FILE)
    df.loc[df['game_id'] == game_id, ['actual_hr', 'status']] = [actual_hr, 'Finished']
    df.to_csv(LOG_FILE, index=False)

# 2. Streamlit UI Logic
st.set_page_config(page_title="ProAnalytics Dashboard", layout="wide")
st.title("⚾ ProAnalytics Performance Tracker")

initialize_log()

# Sidebar for controls
st.sidebar.header("Dashboard Controls")
if st.sidebar.button("Refresh Results"):
    st.rerun()

# 3. Display Performance Table
st.subheader("Prediction vs. Actual Results")
logs = pd.read_csv(LOG_FILE)

# Color-coding logic for quick audit
def color_status(val):
    color = 'green' if val == 'Finished' else 'orange'
    return f'background-color: {color}'

st.dataframe(
    logs.style.applymap(color_status, subset=['status']),
    use_container_width=True
)

# 4. Summary Metrics
if not logs.empty:
    finished_games = logs[logs['status'] == 'Finished']
    if not finished_games.empty:
        accuracy = (finished_games['pred_hr'] == finished_games['actual_hr']).mean() * 100
        st.metric("Model Hit Rate", f"{accuracy:.1f}%")
