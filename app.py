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
                    # Safely drill into nested JSON
                    home = game.get('teams', {}).get('home', {})
                    away = game.get('teams', {}).get('away', {})
                    
                    # Extract players if 'lineups' or 'pitchers' were hydrated
                    # Using .get('lineup', []) and .get('pitchers', [])
                    h_hitters = [p.get('fullName') for p in home.get('lineup', [])]
                    a_hitters = [p.get('fullName') for p in away.get('lineup', [])]
                    
                    games_list.append({
                        'gamePk': game.get('gamePk'),
                        'date': entry.get('date'),
                        'matchup': f"{away.get('team',{}).get('name')} @ {home.get('team',{}).get('name')}",
                        'status': game.get('status', {}).get('detailedState'),
                        'hitters': (h_hitters + a_hitters) or ['No lineup yet'],
                        'pitchers': ['TBD'] # Pitchers often require a separate lookup
                    })
            return games_list
        except: return []

st.set_page_config(layout="wide")
st.title("⚾ ProAnalytics Tracker")

# 1. Show Schedules
matchups = load_matchup_data()
df = pd.DataFrame(matchups)

if not df.empty:
    st.subheader("Upcoming Slate")
    st.dataframe(df.drop(columns=['hitters', 'pitchers']), use_container_width=True)

    # 2. Prediction Form
    with st.form("pred_form"):
        # Filter out 'Postponed'
        active = [m for m in matchups if m['status'] != 'Postponed']
        selection = st.selectbox("Select Game", [m['matchup'] + f" ({m['date']})" for m in active])
        
        # Find selected game data
        game_data = next(m for m in active if m['matchup'] in selection)
        
        hitter = st.selectbox("Select Hitter", game_data['hitters'])
        hr = st.number_input("Predicted HRs", 0)
        
        if st.form_submit_button("Log"):
            st.write(f"Logged {hitter} for {game_data['matchup']}")
else:
    st.warning("No data. Run the collector first.")
