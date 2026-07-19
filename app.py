import streamlit as st
import pandas as pd
import json
import os

# Constants
LOG_FILE = 'predictions_log.csv'
MATCHUP_FILE = 'data/today_matchups.json'

def load_matchup_data():
    """Parses the local JSON file for games, rosters, and scores."""
    if not os.path.exists(MATCHUP_FILE): 
        return []
    
    try:
        with open(MATCHUP_FILE, 'r') as f:
            data = json.load(f)
            games_list = []
            
            for entry in data.get('dates', []):
                for game in entry.get('games', []):
                    home = game.get('teams', {}).get('home', {})
                    away = game.get('teams', {}).get('away', {})
                    
                    # Score extraction
                    h_score = home.get('score', 0)
                    a_score = away.get('score', 0)
                    
                    # Safely drill into the 'lineup' list -> 'person' dict -> 'fullName'
                    h_hitters = [p.get('person', {}).get('fullName') for p in home.get('lineup', [])]
                    a_hitters = [p.get('person', {}).get('fullName') for p in away.get('lineup', [])]
                    
                    all_hitters = h_hitters + a_hitters
                    
                    games_list.append({
                        'date': entry.get('date'),
                        'matchup': f"{away.get('team',{}).get('name')} vs {home.get('team',{}).get('name')}",
                        'status': game.get('status', {}).get('detailedState', 'Scheduled'),
                        'score': f"{a_score} - {h_score}" if game.get('status', {}).get('abstractGameState') == 'Final' else "N/A",
                        'hitters': all_hitters if all_hitters else ['Lineup pending'],
                        'gamePk': game.get('gamePk')
                    })
            return games_list
    except (json.JSONDecodeError, KeyError, Exception):
        return []

# App Configuration
st.set_page_config(page_title="ProAnalytics", layout="wide")
st.title("⚾ ProAnalytics Performance Tracker")

matchups = load_matchup_data()

if matchups:
    df = pd.DataFrame(matchups)
    st.subheader("Upcoming Slate & Scores")
    # Displays date, matchup, status, and the new score column
    st.dataframe(df[['date', 'matchup', 'status', 'score']], hide_index=True, width='stretch')

    # Prediction Form
    st.subheader("Add New Prediction")
    with st.form("pred_form"):
        active_games = [m for m in matchups if m['status'] != 'Postponed']
        
        if not active_games:
            st.warning("No active games available for predictions.")
        else:
            selected = st.selectbox("Select Matchup", [f"{m['date']} | {m['matchup']}" for m in active_games])
            game = next(m for m in active_games if f"{m['date']} | {m['matchup']}" == selected)
            
            hitter = st.selectbox("Select Hitter", game['hitters'])
            hr = st.number_input("Predicted Home Runs", min_value=0, step=1)
            
            if st.form_submit_button("Log Prediction"):
                if hitter == 'Lineup pending':
                    st.error("Cannot log: Lineup data is not yet available.")
                else:
                    new_entry = pd.DataFrame([{
                        'date': game['date'], 
                        'matchup': game['matchup'], 
                        'hitter': hitter, 
                        'hr': hr
                    }])
                    new_entry.to_csv(
                        LOG_FILE, 
                        mode='a', 
                        header=not os.path.exists(LOG_FILE), 
                        index=False
                    )
                    st.success(f"Successfully logged {hr} HR(s) for {hitter}!")
else:
    st.warning("Data not found. Ensure the collector script has run.")
