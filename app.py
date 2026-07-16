import streamlit as st
import pandas as pd
import requests

# ... (Previous imports and setup)

def load_data():
    # Fetch your JSON (ensure this uses the 'today_matchups.json' path)
    response = requests.get(DATA_URL)
    data = response.json()
    
    matchups = []
    for game in data['dates'][0]['games']:
        # Extract pitcher stats from the new JSON structure
        home = game['teams']['home']
        away = game['teams']['away']
        
        matchups.append({
            "Matchup": f"{away['team']['name']} vs {home['team']['name']}",
            "Home Pitcher (ERA)": f"{home['pitcher_stats']['name']} ({home['pitcher_stats']['era']})",
            "Away Pitcher (ERA)": f"{away['pitcher_stats']['name']} ({away['pitcher_stats']['era']})",
            "Status": game['status']['detailedState']
        })
    return pd.DataFrame(matchups)

df = load_data()

if df is not None:
    st.write("### ⚾ Today's SharpPLAY Matchups & Pitching")
    st.dataframe(df, use_container_width=True, hide_index=True)
