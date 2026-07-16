import streamlit as st
import pandas as pd
import requests

# --- CORRECTED: Define your raw data URL here ---
# Ensure you use your actual GitHub username and repository name
[https://raw.githubusercontent.com/carter6tyreen-byte/SharpPlay-Analytics/main/today_matchups.json](https://raw.githubusercontent.com/carter6tyreen-byte/SharpPlay-Analytics/main/today_matchups.json)⁠

def load_data():
    try:
        response = requests.get(DATA_URL)
        response.raise_for_status() # Check for errors
        data = response.json()
        
        matchups = []
        # Update this path if your JSON structure differs
        for game in data.get('dates', [{}])[0].get('games', []):
            home = game['teams']['home']
            away = game['teams']['away']
            
            matchups.append({
                "Matchup": f"{away['team']['name']} vs {home['team']['name']}",
                "Home Pitcher": home.get('pitcher_stats', {}).get('name', 'N/A'),
                "Away Pitcher": away.get('pitcher_stats', {}).get('name', 'N/A'),
                "Status": game['status']['detailedState']
            })
        return pd.DataFrame(matchups)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

st.title("SharpPLAY Analytics Dashboard")
df = load_data()

if df is not None:
    st.write("### ⚾ Today's Matchups")
    st.dataframe(df, use_container_width=True, hide_index=True)
