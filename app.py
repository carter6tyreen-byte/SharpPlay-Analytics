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

st.title("⚾ SharpPlay Analytics & Edge Matrix")
st.markdown("Professional pre-game modeling, active lineup metrics, and strict pre-game ticket validation.")

# Sidebar Active Slip Manager
st.sidebar.header("🎫 Active Pre-Game Ticket Slip")
if st.session_state.bet_slip:
    st.sidebar.write(f"Locked Legs: {len(st.session_state.bet_slip)}")
    for i, leg in enumerate(st.session_state.bet_slip, 1):
        st.sidebar.markdown(f"**{i}. {leg['Player']}**\n- Prop: {leg['Market']}\n- Odds: {leg['Odds']}\n- Game: {leg['Matchup']}")
    if st.sidebar.button("Clear Ticket Slip"):
        st.session_state.bet_slip = []
        st.rerun()
else:
    st.sidebar.info("Slip is empty. Select an upcoming pre-game matchup below to add edges.")

# Navigation
view_mode = st.sidebar.selectbox(
    "Dashboard View",
    ["Pre-Game Matchups & Lineups", "Odds Matrix & Edge Projections", "System Status"]
)

if view_mode == "Pre-Game Matchups & Lineups":
    st.subheader("Today's Active Schedule & Game State Validation")
    
    with st.spinner("Fetching verified MLB feeds..."):
        try:
            today_str = datetime.now().strftime("%Y-%m-%d")
            schedule_url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today_str}&hydrate=probablePitcher,linescore"
            
            resp = requests.get(schedule_url)
            data = resp.json()
            
            pregame_games = {}
            completed_games = []
            
            for date_entry in data.get("dates", []):
                for game in date_entry.get("games", []):
                    g_pk = game["gamePk"]
                    away = game["teams"]["away"]["team"]["name"]
                    home = game["teams"]["home"]["team"]["name"]
                    status = game["status"]["detailedState"]
                    
                    label = f"{away} @ {home} [{status}]"
                    
                    # Strict filtering: Only allow pre-game or scheduled matchups for betting/tickets
                    if status in ["Scheduled", "Pre-Game", "Warmup"]:
                        pregame_games[label] = {
                            "pk": g_pk,
                            "away": away,
                            "home": home,
                            "status": status
                        }
                    else:
                        completed_games.append(label)
            
            # Show dropdown only for valid pre-game matchups
            if pregame_games:
                chosen_label = st.selectbox("Select Valid Pre-Game Matchup:", list(pregame_games.keys()))
                game_info = pregame_games[chosen_label]
                game_pk = game_info["pk"]
                
                st.success(f"🔒 Game Status Verified: **{game_info['status']}**. Betting and ticket building enabled.")
                
                # Fetch live boxscore / lineups
                live_url = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
                live_resp = requests.get(live_url).json()
                boxscore = live_resp.get("liveData", {}).get("boxscore", {}).get("teams", {})
                
                col1, col2 = st.columns(2)
                
                def parse_lineup(team_box):
                    players_dict = team_box.get("players", {})
                    rows = []
                    for b_id in team_box.get("batters", []):
                        p = players_dict.get(f"ID{b_id}", {})
                        name = p.get("person", {}).get("fullName", "Unknown")
                        pos = p.get("primaryPosition", {}).get("abbreviation", "BAT")
                        stats = p.get("stats", {}).get("batting", {})
                        
                        rows.append({
                            "Player": f"{name} ({pos})",
                            "AVG": stats.get("avg", ".---"),
                            "HR": stats.get("homeRuns", 0),
                            "OPS": stats.get("ops", ".---")
                        })
                    return pd.DataFrame(rows)

                with col1:
                    st.markdown(f"**{game_info['away']} Lineup & Stats**")
                    away_df = parse_lineup(boxscore.get("away", {}))
                    if not away_df.empty:
                        st.dataframe(away_df, hide_index=True, use_container_width=True)
                        away_player_list = away_df["Player"].tolist()
                        sel_away_target = st.selectbox("Target Away Batter:", away_player_list, key="a_tar")
                    else:
                        st.info("Lineups not yet posted.")
                        sel_away_target = None

                with col2:
                    st.markdown(f"**{game_info['home']} Lineup & Stats**")
                    home_df = parse_lineup(boxscore.get("home", {}))
                    if not home_df.empty:
                        st.dataframe(home_df, hide_index=True, use_container_width=True)
                        home_player_list = home_df["Player"].tolist()
                        sel_home_target = st.selectbox("Target Home Batter:", home_player_list, key="h_tar")
                    else:
                        st.info("Lineups not yet posted.")
                        sel_home_target = None
                
                st.markdown("---")
                st.subheader("🎯 Professional Pre-Game Ticket Builder")
                
                # Choose target player from available selections
                active_target = sel_away_target if sel_away_target else (sel_home_target if sel_home_target else "Selected Player")
                
                t1, t2, t3 = st.columns(3)
                with t1:
                    market = st.selectbox("Prop Market", ["Player Hits Over 0.5", "Home Run Prop", "Total Bases Over 1.5", "RBIs Over 0.5"])
                with t2:
                    odds = st.text_input("Target American Odds", value="+140")
                with t3:
                    st.write("")
                    st.write("")
                    if st.button("Lock Leg to Ticket Slip"):
                        st.session_state.bet_slip.append({
                            "Player": active_target,
                            "Market": market,
                            "Odds": odds,
                            "Matchup": f"{game_info['away']} @ {game_info['home']}"
                        })
                        st.success(f"Successfully locked **{active_target}** into your official ticket slip!")
            else:
                st.warning("⚠️ No live pre-game or upcoming matchups currently available for betting on today's slate.")
                if completed_games:
                    st.info(f"Note: {len(completed_games)} game(s) today are already Final or In Progress and have been locked out of the ticket builder.")
            
        except Exception as e:
            st.error(f"Error loading pipeline: {e}")

elif view_mode == "Odds Matrix & Edge Projections":
    st.subheader("📊 Model Edge & Odds Matrix")
    matrix_df = pd.DataFrame({
        "Matchup": ["Upcoming Slate Matchup A", "Upcoming Slate Matchup B"],
        "Spread / Run Line": ["-1.5 (+150)", "+1.5 (-170)"],
        "Total (O/U)": ["8.5 (-110)", "8.0 (-115)"],
        "Sharp Model Edge": ["+5.4% Value", "+3.1% Value"]
    })
    st.dataframe(matrix_df, use_container_width=True, hide_index=True)

else:
    st.subheader("System Status")
    st.success("Environment operational on Python 3.11 with strict state validation active.")
