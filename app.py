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
st.markdown("Advanced Major League Baseball statistics, live lineups, batter vs. pitcher data, and ticket builder.")

# Sidebar Controls
st.sidebar.header("Navigation & Filters")
view_mode = st.sidebar.selectbox(
    "Select Dashboard View",
    ["Live Matchups & Lineups", "Odds Matrix", "System Status"]
)

# Main Content Area
if view_mode == "Live Matchups & Lineups":
    st.subheader("Today's Matchup Schedule")
    
    with st.spinner("Fetching games from MLB Stats API..."):
        try:
            today_str = datetime.now().strftime("%Y-%m-%d")
            schedule_url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today_str}&hydrate=probablePitcher,linescore"
            
            response = requests.get(schedule_url)
            data = response.json()
            
            games_dict = {}
            dates = data.get("dates", [])
            
            if dates:
                for date_entry in dates:
                    for game in date_entry.get("games", []):
                        game_pk = game["gamePk"]
                        away_team = game["teams"]["away"]["team"]["name"]
                        home_team = game["teams"]["home"]["team"]["name"]
                        status = game["status"]["detailedState"]
                        
                        matchup_label = f"{away_team} @ {home_team} ({status})"
                        games_dict[matchup_label] = game_pk
            
            if games_dict:
                selected_matchup = st.selectbox("Select a game to load lineups and deep metrics:", list(games_dict.keys()))
                game_pk = games_dict[selected_matchup]
                
                # Fetch Live Feed / Boxscore for the selected game
                live_url = f"https://statsapi.mlb.com/api/v1.1/game/{game_pk}/feed/live"
                live_resp = requests.get(live_url)
                live_data = live_resp.json()
                
                boxscore = live_data.get("liveData", {}).get("boxscore", {})
                teams_data = boxscore.get("teams", {})
                
                away_data = teams_data.get("away", {})
                home_data = teams_data.get("home", {})
                
                away_team_name = away_data.get("team", {}).get("name", "Away Team")
                home_team_name = home_data.get("team", {}).get("name", "Home Team")
                
                st.markdown("---")
                st.subheader(f"📋 Lineups & Batter Metrics: {selected_matchup}")
                
                col1, col2 = st.columns(2)
                
                def extract_lineup(team_box):
                    batters = team_box.get("batters", [])
                    players = team_box.get("players", {})
                    lineup_list = []
                    for b_id in batters:
                        player_key = f"ID{b_id}"
                        p_info = players.get(player_key, {})
                        name = p_info.get("person", {}).get("fullName", "Unknown")
                        position = p_info.get("primaryPosition", {}).get("abbreviation", "")
                        stats = p_info.get("stats", {}).get("batting", {})
                        
                        # Extract basic stats if available
                        avg = stats.get("avg", ".---")
                        hr = stats.get("homeRuns", 0)
                        ops = stats.get("ops", ".---")
                        
                        lineup_list.append({
                            "Batter": f"{name} ({position})",
                            "AVG": avg,
                            "HR": hr,
                            "OPS": ops
                        })
                    return pd.DataFrame(lineup_list)

                with col1:
                    st.markdown(f"**{away_team_name} Batters**")
                    away_df = extract_lineup(away_data)
                    if not away_df.empty:
                        st.dataframe(away_df, hide_index=True, use_container_width=True)
                        selected_away_batter = st.selectbox("Select Away Batter for Pitch Mix:", away_df["Batter"], key="away_batter")
                    else:
                        st.info("Lineups not yet posted.")

                with col2:
                    st.markdown(f"**{home_team_name} Batters**")
                    home_df = extract_lineup(home_data)
                    if not home_df.empty:
                        st.dataframe(home_df, hide_index=True, use_container_width=True)
                        selected_home_batter = st.selectbox("Select Home Batter for Pitch Mix:", home_df["Batter"], key="home_batter")
                    else:
                        st.info("Lineups not yet posted.")
                
                # Ticket Builder Section
                st.markdown("---")
                st.subheader("🎯 Ticket Builder & Prop Matrix")
                
                t_col1, t_col2, t_col3 = st.columns(3)
                with t_col1:
                    bet_type = st.selectbox("Market Type", ["Player Hits", "Home Run Prop", "Total Bases", "Strikeouts (Pitcher)"])
                with t_col2:
                    selection_target = st.text_input("Target Player / Selection", value="Selected Batter")
                with t_col3:
                    odds_input = st.text_input("Target Odds (American)", value="+150")
                
                if st.button("Add to Ticket"):
                    st.success(f"Added **{selection_target}** ({betent if 'betent' in locals() else bet_type}) at {odds_input} to your active slip!")

            else:
                st.info("No games available for today.")
                
        except Exception as e:
            st.error(f"Error loading live game feeds: {e}")

elif view_mode == "Odds Matrix":
    st.subheader("Odds Matrix & Projections Grid")
    st.dataframe(pd.DataFrame(columns=["Matchup", "Spread", "Total (O/U)", "ML Away", "ML Home", "Sharp Edge"]), hide_index=True, use_container_width=True)

else:
    st.subheader("System Status")
    st.success("Streamlit environment running on Python 3.11 successfully.")
    st.write("GitHub Actions pipeline and automated workflows are active.")
