import streamlit as st
import requests
import datetime
import pandas as pd

st.set_page_config(page_title="SharpPlay Analytics: ODE Optimizer", layout="wide")

st.title("SharpPlay Analytics: ODE Optimizer")

# 1. Fetch Today's Live Scoreboard / Slate from MLB API
today = datetime.date.today().strftime("%Y-%m-%d")
schedule_url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today}&hydrate=team,linescore"

games_list = []
try:
    resp = requests.get(schedule_url, timeout=10)
    data = resp.json()
    dates = data.get("dates", [])
    if dates:
        for game in dates[0].get("games", []):
            game_id = game.get("gamePk")
            away_team = game.get("teams", {}).get("away", {}).get("team", {}).get("name", "Away")
            home_team = game.get("teams", {}).get("home", {}).get("team", {}).get("name", "Home")
            status = game.get("status", {}).get("detailedState", "Scheduled")
            games_list.append({
                "gamePk": game_id,
                "matchup": f"{away_team} @ {home_team}",
                "status": status,
                "away": away_team,
                "home": home_team
            })
except Exception as e:
    st.error(f"Error loading MLB scoreboard: {e}")

st.subheader("Today's Full Slate Scoreboard")

if not games_list:
    st.info("No games found on today's slate or API limit reached. Showing sample matchup view.")
    games_list = [{"gamePk": 0, "matchup": "New York Yankees @ Boston Red Sox", "status": "Preview", "away": "New York Yankees", "home": "Boston Red Sox"}]

# Display Scoreboard selection buttons / interactive layout
selected_game = None
for g in games_list:
    cols = st.columns([3, 2, 2])
    with cols[0]:
        st.write(f"**{g['matchup']}**")
    with cols[1]:
        st.caption(f"Status: {g['status']}")
    with cols[2]:
        if st.button("View Matchup", key=f"game_{g['gamePk']}"):
            selected_game = g

# Divider for Detailed View
st.markdown("---")

if selected_game:
    st.header(f"Matchup Deep Dive: {selected_game['matchup']}")
    
    # 2. Color-coded grades, percentages, pitch mix, and pitcher vs batter breakdown
    tab_overview, tab_pitcher_batter, tab_pitch_mix = st.tabs(["Overview & Grades", "Pitcher vs Batter", "Pitch Mix Breakdown"])
    
    with tab_overview:
        st.subheader("Color-Coded Matchup Grades")
        # Simulating clean color-coded metric cards / dataframe
        overview_data = pd.DataFrame({
            "Metric": ["Overall Matchup Grade", "Power Index (ISO)", "Contact Rate", "Chase Rate", "ODE Optimization Score"],
            "Away Team (" + selected_game['away'] + ")": ["B+", "74", "78%", "24%", "82.4"],
            "Home Team (" + selected_game['home'] + ")": ["A-", "81", "82%", "21%", "88.1"]
        })
        st.dataframe(overview_data, use_container_width=True)
        
    with tab_pitcher_batter:
        st.subheader("Pitcher vs Batter Comparative Board")
        col_p, col_b = st.columns(2)
        with col_p:
            st.markdown("#### Starting Pitcher Profile")
            st.info("Name: Ace RHP\n* ERA: 3.12\n* WHIP: 1.05\n* K/9: 10.4\n* Hard-Hit %: 31.2%")
        with col_b:
            st.markdown("#### Lineup Key Hitters")
            st.success("Core Metrics:\n* wOBA vs RHP: .350\n* Barrel %: 14.2%\n* Exit Velocity: 91.5 mph")
            
    with tab_pitch_mix:
        st.subheader("Pitch Mix & Usage Analytics")
        pitch_mix_df = pd.DataFrame({
            "Pitch Type": ["Fastball (4SFB)", "Slider", "Changeup", "Curveball"],
            "Usage %": ["45%", "28%", "17%", "10%"],
            "Whiff %": ["25%", "38%", "33%", "30%"],
            "Run Value": ["+2.1", "+4.5", "+1.2", "+0.8"]
        })
        st.dataframe(pitch_mix_df, use_container_width=True)
else:
    st.info("👆 Click **'View Matchup'** on any game above to open the full color-graded breakdown, pitcher vs. batter stats, and pitch mix analysis.")
