import streamlit as st
import statsapi
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(page_title="SharpPlay Analytics - MLB Matchups", layout="wide")

st.title("⚾ SharpPlay Analytics: Today's Matchups & Home Run Props")

# Get today's date formatted correctly for the MLB Stats API (MM/DD/YYYY)
today_str = datetime.now().strftime("%m/%d/%Y")
st.sidebar.header("Configuration")
selected_date = st.sidebar.text_input("Query Date (MM/DD/YYYY)", value=today_str)

@st.cache_data
def fetch_mlb_schedule(date_str):
    try:
        # Fetch raw schedule data using explicit date bounds
        schedule = statsapi.schedule(start_date=date_str, end_date=date_str)
        return schedule
    except Exception as e:
        st.error(f"Error fetching schedule: {e}")
        return []

# Fetch schedule data
games = fetch_mlb_schedule(selected_date)

if not games:
    st.warning(f"No games found or empty results returned for date: {selected_date}. Please check the date format or try a different date.")
else:
    st.success(f"Successfully loaded {len(games)} games for {selected_date}!")
    
    matchup_list = []
    for game in games:
        matchup_list.append({
            "Game": f"{game.get('away_name', 'Away')} @ {game.get('home_name', 'Home')}",
            "Time": game.get('game_time', 'TBD'),
            "Venue": game.get('venue_name', 'Unknown'),
            "Status": game.get('status', 'Scheduled')
        })
    
    df_games = pd.DataFrame(matchup_list)
    
    # Render dataframe with proper sizing
    st.dataframe(df_games, width='stretch')
