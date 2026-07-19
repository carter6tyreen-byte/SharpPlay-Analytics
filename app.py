import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuration
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
        'actual_hr': 0, 
        'status': 'Pending'
    }
    df = pd.DataFrame([new_data])
    df.to_csv(LOG_FILE, mode='a', header=False, index=False)

# UI Display
st.set_page_config(page_title="ProAnalytics Dashboard", layout="wide")
st.title("⚾ ProAnalytics Performance Tracker")

initialize_log()

# Sidebar for manual testing
st.sidebar.header("Add Prediction")
with st.sidebar.form("predict_form"):
    gid = st.text_input("Game ID")
    hit = st.text_input("Batter Name")
    hr = st.number_input("Predicted HRs", min_value=0)
    if st.form_submit_button("Log Entry"):
        log_prediction(gid, "N/A", hit, hr)
        st.success("Logged!")
        st.rerun()

# Performance Display
st.subheader("Prediction vs. Actual Results")
logs = pd.read_csv(LOG_FILE)

# Styling function
def color_status(val):
    color = 'green' if val == 'Finished' else 'orange'
    return f'background-color: {color}'

# Updated to use width='stretch' per Streamlit's new requirements
st.dataframe(
    logs.style.map(color_status, subset=['status']),
    width='stretch' 
)

if not logs.empty:
    finished = logs[logs['status'] == 'Finished']
    if not finished.empty:
        acc = (finished['pred_hr'] == finished['actual_hr']).mean() * 100
        st.metric("Model Hit Rate", f"{acc:.1f}%")
