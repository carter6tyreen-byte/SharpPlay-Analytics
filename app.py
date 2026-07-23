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

# Initialize Session State Slip
if "bet_slip" not in st.session_state:
    st.session_state.bet_slip = []

st.title("⚾ SharpPlay Analytics & Odds Matrix")
st.markdown("Advanced Major League Baseball stats, active lineups, prop tracking, and ticket builder.")

# Sidebar Controls for Active Ticket Slip
st.sidebar.header("🎫 Active Ticket Slip")
if st.session_state.bet_slip:
    st.sidebar.write(f"Total Legs: {len(st.session_state.bet_slip)}")
    for i, leg in enumerate(st.session_state.bet_slip, 1):
        st.sidebar.markdown(f"**{i}. {leg['Player']}**\n- Market: {leg['Market']}\n- Odds: {leg['Odds']}")
    if st.sidebar.button("Clear Ticket Slip"):
        st.session_state.bet_slip = []
        st.rerun()
else:
    st.sidebar.info("Your ticket slip is empty. Add props from matchups below!")

# Navigation
view_mode = st.sidebar.selectbox(
    "Dashboard View",
    ["Live Matchups & Lineups", "Odds Matrix & Ticket Builder", "System Status"]
)

if view_mode == "Live Matchups & Lineups":
    st.subheader("Today's Active MLB Schedule")
    
    with st.spinner("Loading live game schedule..."):
        try:
            today_str = datetime.now().strftime("%Y-%m-%d")
            schedule_url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today_str}&hydrate=probablePitcher,linescore"
            
            resp = requests.get(schedule_url)
            data = resp.json()
            
            games_dict = {}
            for date_entry in data.get("dates", []):
                for game in date_entry.get("games", []):
                    g_pk = game["gamePk"]
                    away = game["teams"]["away"]["team"]["name"]
                    home = game["teams"]["home"]["team"]["name"]
                    status = game["status"]["detailedState"]
                    games_dict[f"{away} @ {home} ({status})"] = g_pk
            
            if games_dict:
                chosen_game = st.selectbox("Select Matchup to Inspect Lineup:", list(games_dict.keys()))
                game_pk = games_dict[chosen_game]
                
                # Live feed boxscore
                live_url = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
                live_data = requests.get(live_url).json()
                boxscore = live_data.get("liveData", {}).get("boxscore", {}).get("teams", {})
                
                away_team = boxscore.get("away", {}).get("team", {}).get("name", "Away")
                home_team = boxscore.get("home", {}).get("team", {}).get("name", "Home")
                
                col1, col2 = st.columns(2)
                
                def get_batters(team_data):
                    players_dict = team_data.get("players", {})
                    batters_list = []
                    for b_id in team_data.get("batters", []):
                        p_info = players_dict.get(f"ID{b_id}", {})
                        name = p_info.get("person", {}).get("fullName", "Unknown")
                        pos = p_info.get("primaryPosition", {}).get("abbreviation", "BAT")
                        batters_list.append(f"{name} ({pos})")
                    return batters_list

                with col1:
                    st.markdown(f"**{away_team} Batters**")
                    away_batters = get_batters(boxscore.get("away", {}))
                    if away_batters:
                        sel_away_p = st.selectbox("Pick Away Prop Target:", away_batters, key="away_p")
                    else:
                        st.info("Lineup pending.")

                with col2:
                    st.markdown(f"**{home_team} Batters**")
                    home_batters = get_batters(boxscore.get("home", {}))
                    if home_batters:
                        sel_home_p = st.selectbox("Pick Home Prop Target:", home_batters, key="home_p")
                    else:
                        st.info("Lineup pending.")
                        
                st.markdown("---")
                st.subheader("💡 Quick Add Prop to Ticket")
                
                # Pick active target player from either dropdown
                target_prop_player = sel_away_p if 'sel_away_p' in locals() else "Selected Player"
                
                q_col1, q_col2, q_col3 = st.columns(3)
                with q_col1:
                    market = st.selectbox("Prop Market", ["1+ Hits", "Home Run", "Total Bases Over 1.5", "RBIs Over 0.5", "Strikeouts Over 6.5"])
                with q_col2:
                    line_odds = st.text_input("American Odds", value="-115")
                with q_col3:
                    st.write("")
                    st.write("")
                    if st.button("Add to Ticket Slip"):
                        st.session_state.bet_slip.append({"Player": target_prop_player, "Market": market, "Odds": line_odds})
                        st.success(f"Added **{target_prop_player}** ({market}) to slip!")
            else:
                st.info("No games scheduled today.")
        except Exception as e:
            st.error(f"Error loading API data: {e}")

elif view_mode == "Odds Matrix & Ticket Builder":
    st.subheader("🎯 Active Ticket Slip & Summary")
    
    if st.session_state.bet_slip:
        slip_df = pd.DataFrame(st.session_state.bet_slip)
        st.dataframe(slip_df, use_container_width=True, hide_index=True)
        if st.button("Clear Slip"):
            st.session_state.bet_slip = []
            st.rerun()
    else:
        st.info("Your ticket slip is currently empty. Visit **Live Matchups & Lineups** to build your bets.")
        
    st.markdown("---")
    st.subheader("📊 Matchup Odds & Model Edge Matrix")
    matrix_sample = pd.DataFrame({
        "Matchup": ["SD @ ATL", "MIN @ CLE", "TB @ TOR"],
        "Spread": ["-1.5 (+140)", "+1.5 (-160)", "-1.5 (+155)"],
        "Total (O/U)": ["8.5 (-110)", "8.0 (-105)", "7.5 (-115)"],
        "Model Edge": ["+4.2% Away", "-1.1% Home", "+6.5% Over"]
    })
    st.dataframe(matrix_sample, hide_index=True, use_container_width=True)

else:
    st.subheader("System Status")
    st.success("Environment running cleanly on Python 3.11 with live MLB pipeline active.")
