import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="SharpPlay Analytics",
    page_icon="⚾",
    layout="wide"
)

# App Header
st.title("⚾ SharpPlay Analytics Dashboard")
st.markdown("Live Major League Baseball statistics, data pipelines, and matchup insights.")

# Sidebar Controls
st.sidebar.header("Navigation & Filters")
view_mode = st.sidebar.selectbox(
    "Select Dashboard View",
    ["Live Matchups", "Odds Matrix", "System Status"]
)

# Main Content Area
if view_mode == "Live Matchups":
    st.subheader("Today's MLB Matchup Analytics")
    
    with st.spinner("Fetching live data from MLB Stats API..."):
        try:
            # Get today's date in YYYY-MM-DD format
            today_str = datetime.now().strftime("%Y-%m-%d")
            api_url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today_str}"
            
            response = requests.get(api_url)
            data = response.json()
            
            games_list = []
            if data.get("totalItems", 0) > 0:
                dates = data.get("dates", [])
                if dates:
                    for game in dates[0].get("games", []):
                        away_team = game["teams"]["away"]["team"]["name"]
                        home_team = game["teams"]["home"]["team"]["name"]
                        status = game["status"]["detailedState"]
                        game_time = game.get("gameDate", "")
                        
                        games_list.append({
                            "Matchup": f"{away_team} @ {home_team}",
                            "UTC Time": game_time,
                            "Status": status
                        })
            
            if games_list:
                df_games = pd.DataFrame(games_list)
                st.success(f"Successfully loaded {len(games_list)} games for today!")
                st.table(df_games)
            else:
                st.info("No MLB games scheduled for today or off-season.")
                
        except Exception as e:
            st.error(f"Error fetching live MLB data: {e}")

elif view_mode == "Odds Matrix":
    st.subheader("Odds Matrix & Projections")
    st.write("Viewing current odds matrix configurations.")

else:
    st.subheader("System Status")
    st.success("Streamlit environment running on Python 3.11 successfully.")
    st.write("GitHub Actions pipeline and automated workflows are active.")
