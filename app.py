import streamlit as st
import pandas as pd
import json
import os

LOG_FILE = 'predictions_log.csv'
MATCHUP_FILE = 'data/today_matchups.json'

def load_matchup_data():
    if not os.path.exists(MATCHUP_FILE): return []
    with open(MATCHUP_FILE, 'r') as f:
        try:
            data = json.load(f)
            games_list = []
            for entry in data.get('dates', []):
                for game in entry.get('games', []):
                    home = game.get('teams', {}).get('home', {})
                    away = game.get('teams', {}).get('away', {})
                    
                    # Extract names from hydrated lineup/pitcher lists
                    h_hitters = [p.get('fullName') for p in home.get('lineup', [])]
                    a_hitters = [p.get('fullName') for p in away.get('lineup', [])]
                    
                    games_list.append({
                        'date': entry.get('date'),
                        'matchup': f"{away.get('team',{}).get('name')} vs {home.get('team',{}).get('name')}",
                        'status': game.get('status', {}).get('detailedState', 'Scheduled'),
                        'hitters': (h_hitters + a_hitters) or ['Lineup pending'],
                        'gamePk': game.get('gamePk')
                    })
            return games_list
        except: return []

st.set_page_config(page_title="ProAnalytics", layout="wide")
st.title("⚾ ProAnalytics Performance Tracker")

matchups = load_matchup_data()

if matchups:
    df = pd.DataFrame(matchups)
    st.subheader("Upcoming Slate (Today & Tomorrow)")
    st.dataframe(df[['date', 'matchup', 'status']], width='stretch')

    st.subheader("Add New Prediction")
    with st.form("pred_form"):
        active = [m for m in matchups if m['status'] != 'Postponed']
        selected = st.selectbox("Select Matchup", [f"{m['date']} | {m['matchup']}" for m in active])
        game = next(m for m in active if f"{m['date']} | {m['matchup']}" == selected)
        
        hitter = st.selectbox("Select Hitter", game['hitters'])
        hr = st.number_input("Predicted HRs", 0, step=1)
        
        if st.form_submit_button("Log Prediction"):
            if hitter == 'Lineup pending':
                st.error("Lineup not yet available.")
            else:
                pd.DataFrame([{'date': game['date'], 'matchup': game['matchup'], 'hitter': hitter, 'hr': hr}]).to_csv(
                    LOG_FILE, mode='a', header=not os.path.exists(LOG_FILE), index=False
                )
                st.success(f"Logged {hitter}!")
else:
    st.warning("Run the data collector first.")
ok 
