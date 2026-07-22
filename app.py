import datetime
import json
import os
import streamlit as st

# Define tabs at the top
tab_today, tab_tomorrow = st.tabs(
    ["⚡ Today's Slate & Grades", "🔮 Tomorrow's Preview & Lineups"]
)

with tab_today:
  st.subheader("⚡ Today's Live Slate & Scoreboard")
  # Your existing today view code goes here...

with tab_tomorrow:
  st.subheader("📋 Next Slate Matchups & Projected Lineups")

  # Calculate tomorrow's date dynamically
  tomorrow_date = (
      datetime.date.today() + datetime.timedelta(days=1)
  ).strftime("%Y-%m-%d")
  st.caption(f"Loading scheduled games and lineups for: {tomorrow_date}")

  # Safe file loader matching your data directory structure
  file_path = f"data/slate_{tomorrow_date}.json"

  upcoming_games = []
  if os.path.exists(file_path):
    try:
      with open(file_path, "r") as f:
        upcoming_games = json.load(f)
    except Exception as e:
      st.error(f"Error parsing schedule file: {e}")

  if not upcoming_games:
    st.info(
        f"Projected lineups and data for {tomorrow_date} are still pending or"
        " awaiting the scheduled GitHub Actions workflow update."
    )
  else:
    for game in upcoming_games:
      away_team = game.get("away_team", "Away")
      home_team = game.get("home_team", "Home")
      game_time = game.get("game_time", "TBD")

      with st.expander(f"{away_team} @ {home_team} ({game_time})"):
        col1, col2 = st.columns(2)

        with col1:
          st.markdown(
              f"**Away Lineup ({away_team})**<br>Starting Pitcher: *"
              f"{game.get('away_probable_pitcher', 'TBD')}*",
              unsafe_allow_html=True,
          )

        with col2:
          st.markdown(
              f"**Home Lineup ({home_team})**<br>Starting Pitcher: *"
              f"{game.get('home_probable_pitcher', 'TBD')}*",
              unsafe_allow_html=True,
          )
