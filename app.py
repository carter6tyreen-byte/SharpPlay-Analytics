import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Updated with the exact path identified in your system metadata
DATA_URL = "https://raw.githubusercontent.com/carter6tyreen-byte/SharpPlay-Analytics/refs/heads/main/data/today_matchups.json"

st.set_page_config(page_title="SharpPLAY Analytics", layout="wide")

@st.cache_data(ttl=3600)
def load_data():
    try:
        response = requests.get(DATA_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Navigate the nested MLB JSON structure: dates -> [0] -> games
        games_list = data.get("dates", [{}])[0].get("games", [])
        
        if not games_list:
            return None
            
        # Flatten the nested structure into a clean DataFrame
        df = pd.json_normalize(games_list)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

st.title("⚾ SharpPLAY Analytics Dashboard")

if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

df = load_data()

if df is not None and not df.empty:
    st.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Selecting columns that exist in the nested structure
    display_cols = [
        'teams.away.team.name', 
        'teams.home.team.name', 
        'venue.name', 
        'status.detailedState', 
        'description'
    ]
    
    available_cols = [c for c in display_cols if c in df.columns]
    
    st.dataframe(
        df[available_cols], 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "teams.away.team.name": "Away Team",
            "teams.home.team.name": "Home Team",
            "venue.name": "Venue",
            "status.detailedState": "Status",
            "description": "Notes"
        }
    )
else:
    st.warning("No matchup data available at the moment.")
