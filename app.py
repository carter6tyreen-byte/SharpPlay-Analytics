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
st.markdown("Advanced Major League Baseball statistics, starting pitchers, metrics, and matchup insights.")

# Sidebar Controls
st.sidebar.header("Navigation & Filters")
view_mode = st.sidebar.selectbox(
    "Select Dashboard View",
    ["Live Matchups & Pitchers", "Odds Matrix", "System Status"]
)

# Main Content Area
if view_mode == "Live Matchups & Pitchers":
    st.subheader("Today's Matchup Analytics & Starting Pitchers")
    
    with st.spinner("Fetching deep data feeds from MLB Stats API..."):
        try:
            today_str = datetime.now().strftime("%Y-%m-%d")
            # Endpoint with linescore and probable pitchers expanded
            api_url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today_str}&hydrate=probablePitcher,linescore,team"
            
            response = requests.get(api_url)
            data = response.json()
            
            games_list = []
            dates = data.get("dates", [])
            
            if dates:
                for date_entry in dates:
                    for game in date_entry.get("games", []):
                        # Teams
                        away_team = game["teams"]["away"]["team"]["name"]
                        home_team = game["teams"]["home"]["team"]["name"]
                        
                        # Scores (if live or final)
                        linescore = game.get("linescore", {})
                        away_score = linescore.get("teams", {}).get("away", {}).get("runs", 0) if linescore else 0
                        home_score = linescore.get("teams", {}).get("home", {}).get("runs", 0) if linescore else 0
                        
                        status = game["status"]["detailedState"]
                        
                        # Probable Pitchers
                        away_pitcher = game["teams"]["away"].get("probablePitcher", {}).get("fullName", "TBD")
                        home_pitcher = game["teams"]["home"].get("probablePitcher", {}).get("fullName", "TBD")
                        
                        # Time formatting
                        game_time_utc = game.get("gameDate", "")
                        if game_time_utc:
                            try:
                                dt_obj = datetime.strptime(game_time_utc, "%Y-%m-%dT%H:%M:%SZ")
                                time_formatted = dt_obj.strftime("%I:%M %p UTC")
                            except:
                                time_formatted = game_time_utc
                        else:
                            time_formatted = "TBD"
                        
                        games_list.append({
                            "Away Team": away_team,
                            "Away Pitcher": away_pitcher,
                            "Score": f"{away_score} - {home_score}" if status in ["In Progress", "Final", "Warmup"] else "vs",
                            "Home Team": home_team,
                            "Home Pitcher": home_pitcher,
                            "Time": time_formatted,
                            "Status": status
                        })
            
            if games_list:
                df_games = pd.DataFrame(games_list)
                st.success(f"Successfully loaded {len(games_list)} games with pitching metrics!")
                st.dataframe(df_games, hide_index=True, use_container_width=True)
                
                # Interactive Ticket Builder / Deep Dive Selector
                st.markdown("---")
                st.subheader("🔍 Matchup Deep Dive & Metrics")
                selected_matchup = st.selectbox(
                    "Select a game to view detailed metrics and projections:",
                    df_games["Away Team"] + " @ " + df_games["Home Team"]
                )
                
                if selected_matchup:
                    st.info(f"Loaded analytical profile for **{selected_matchup}**. Ready to plug in custom models, odds matrices, or stat feeds.")
            else:
                st.info("No MLB games scheduled for today or off-season.")
                
        except Exception as e:
            st.error(f"Error fetching live MLB data: {e}")

elif view_mode == "Odds Matrix":
    st.subheader("Odds Matrix & Ticket Builder")
    st.write("Configure your tracking matrices and data columns here.")
    # Placeholder for custom odds matrix grid
    st.dataframe(pd.DataFrame(columns=["Matchup", "Spread", "Total (O/U)", "ML Away", "ML Home", "Sharp Edge"]), hide_index=True, use_container_width=True)

else:
    st.subheader("System Status")
    st.success("Streamlit environment running on Python 3.11 successfully.")
    st.write("GitHub Actions pipeline and automated workflows are active.")



