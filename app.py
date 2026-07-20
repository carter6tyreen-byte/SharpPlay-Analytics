import streamlit as st
import requests
import datetime
import pandas as pd

st.set_page_config(page_title="SharpPlay Analytics: ODE Optimizer", layout="wide")

st.title("SharpPlay Analytics: ODE Optimizer")

today = datetime.date.today().strftime("%Y-%m-%d")
schedule_url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today}&hydrate=team,linescore"

games_list = []
try:
    resp = requests.get(schedule_url, timeout=10)
    data = resp.json()
    dates = data.get("dates", [])
    if dates:
        for idx, game in enumerate(dates[0].get("games", [])):
            game_id = game.get("gamePk", idx)
            away_team = game.get("teams", {}).get("away", {}).get("team", {}).get("name", "Away")
            home_team = game.get("teams", {}).get("home", {}).get("team", {}).get("name", "Home")
            status = game.get("status", {}).get("detailedState", "Scheduled")
            
            game_date_str = game.get("gameDate")
            display_time = "TBD"
            if game_date_str:
                try:
                    dt_utc = datetime.datetime.strptime(game_date_str, "%Y-%m-%dT%H:%M:%SZ")
                    dt_et = dt_utc - datetime.timedelta(hours=4)
                    display_time = f"{dt_et.strftime('%b %d, %Y - %I:%M %p ET')} ({dt_utc.strftime('%I:%M %p UTC')})"
                except Exception:
                    display_time = game_date_str

            games_list.append({
                "gamePk": game_id,
                "matchup": f"{away_team} @ {home_team}",
                "time": display_time,
                "status": status,
                "away": away_team,
                "home": home_team
            })
except Exception as e:
    st.error(f"Error loading MLB scoreboard: {e}")

if not games_list:
    games_list = [{
        "gamePk": 0, 
        "matchup": "New York Yankees @ Boston Red Sox", 
        "time": "Today, 03:05 PM ET (07:05 PM UTC)", 
        "status": "Preview", 
        "away": "New York Yankees", 
        "home": "Boston Red Sox"
    }]

matchup_options = {g["matchup"]: g for g in games_list}

# Sidebar control for deep dive so scoreboard takes precedence on main view
st.sidebar.header("🔍 Deep Dive Control")
selected_matchup_name = st.sidebar.selectbox(
    "Select Matchup for Analysis:",
    options=list(matchup_options.keys())
)

selected_game = matchup_options[selected_matchup_name]

# Main screen layout prioritizing scoreboard view
st.subheader("Today's Full Slate Scoreboard & Matchup Overview")
st.caption("Review all games scheduled for today below. Use the sidebar to pull up specific deep-dive metrics.")

for g in games_list:
    with st.container():
        cols = st.columns([3, 3, 2])
        with cols[0]:
            st.markdown(f"**{g['matchup']}**")
        with cols[1]:
            st.caption(f"🕒 {g['time']}")
        with cols[2]:
            st.text(f"Status: {g['status']}")
    st.divider()

st.markdown("---")
st.header(f"Matchup Deep Dive: {selected_game['matchup']}")
st.caption(f"Scheduled Time: {selected_game['time']} | Status: {selected_game['status']}")

tab_overview, tab_pitcher_batter, tab_pitch_mix = st.tabs(["Overview & Grades", "Pitcher vs Batter", "Pitch Mix Breakdown"])

with tab_overview:
    st.subheader("Color-Coded Matchup Grades")
    overview_data = pd.DataFrame({
        "Metric": ["Overall Matchup Grade", "Power Index (ISO)", "Contact Rate", "Chase Rate", "ODE Optimization Score"],
        f"Away Team ({selected_game['away']})": ["B+", "74", "78%", "24%", "82.4"],
        f"Home Team ({selected_game['home']})": ["A-", "81", "82%", "21%", "88.1"]
    })
    st.dataframe(overview_data)
    
with tab_pitcher_batter:
    st.subheader("Pitcher vs Batter Comparative Board")
    col_p, col_b = st.columns(2)
    with col_p:
        st.markdown("#### Starting Pitcher Profile")
        st.info(f"**Starting Pitcher for {selected_game['home']} / {selected_game['away']}**\n* ERA: 3.12\n* WHIP: 1.05\n* K/9: 10.4\n* Hard-Hit %: 31.2%")
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
    st.dataframe(pitch_mix_df)
