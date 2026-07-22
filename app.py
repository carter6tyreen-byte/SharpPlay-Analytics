import datetime
import streamlit as st

# Create top-level tabs for slate navigation
tab_today, tab_tomorrow = st.tabs(
    ["⚡ Today's Slate & Grades", "🔮 Tomorrow's Preview & Lineups"]
)

with tab_tomorrow:
  st.subheader("📋 Next Slate Matchups & Projected Lineups")

  # Calculate tomorrow's date dynamically based on your cron/app run date
  tomorrow_date = (
      datetime.date.today() + datetime.timedelta(days=1)
  ).strftime("%Y-%m-%d")
  st.caption(f"Loading scheduled games and lineups for: {tomorrow_date}")

  # Example loop over tomorrow's games pulled from your data pipeline
  # (Assuming your JSON/API payload includes tomorrow's preview data)
  upcoming_games = fetch_slate_data_for_date(
      tomorrow_date
  )  # Your custom fetch function

  if not upcoming_games:
    st.info(
        "Projected lineups for tomorrow are still populating or pending official"
        " team submission."
    )
  else:
    for game in upcoming_games:
      with st.expander(
          f"{game['away_team']} @ {game['home_team']} ({game['game_time']})"
      ):
        col1, col2 = st.columns(2)

        with col1:
          st.markdown(
              f"**Away Lineup ({game['away_team']})**<br>Starting Pitcher:"
              f" *{game['away_probable_pitcher']}*",
              unsafe_allow_html=True,
          )
          # Render away projected lineup table/list
          st.dataframe(game["away_lineup_df"], hide_index=True)

        with col2:
          st.markdown(
              f"**Home Lineup ({game['home_team']})**<br>Starting Pitcher:"
              f" *{game['home_probable_pitcher']}*",
              unsafe_allow_html=True,
          )
          # Render home projected lineup table/list
          st.dataframe(game["home_lineup_df"], hide_index=True)
