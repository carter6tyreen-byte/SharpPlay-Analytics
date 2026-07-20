import streamlit as st
import statsapi
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(page_title="SharpPlay Analytics - MLB Matchups", layout="wide")

st.title("⚾ SharpPlay Analytics: Today's Matchups & Lineups")

# Date configuration sidebar
today_str = datetime.now().strftime("%m/%d/%Y")
st.sidebar.header("Configuration")
selected_date = st.sidebar.text_input("Query Date (MM/DD/YYYY)", value=today_str)

@st.cache_data
def fetch_mlb_schedule(date_str):
    try:
        # Request schedule including detailed game data
        schedule = statsapi.schedule(start_date=date_str, end_date=date_str)
        return schedule
    except Exception as e:
        st.error(f"Error fetching schedule: {e}")
        return []

games = fetch_mlb_schedule(selected_date)

if not games:
    st.warning(f"No games found for date: {selected_date}.")
else:
    st.success(f"Successfully loaded {len(games)} games for {selected_date}!")
    
    # Game Selector for Lineups & Weather Details
    st.subheader("📋 Game Details, Weather & Lineups")
    
    game_options = {f"{g['away_name']} @ {g['home_name']} (ID: {g['game_id']})": g['game_id'] for g in games}
    selected_game_label = st.selectbox("Select a Matchup to View Details", options=list(game_options.keys()))
    selected_game_id = game_options[selected_game_label]
    
    # Fetch extended boxscore/game data for weather and lineups
    try:
        boxscore = statsapi.boxscore_data(selected_game_id)
        game_status_data = statsapi.get("game", {"gamePk": selected_game_id})
        
        # Extract Weather info if available
        weather_info = game_status_data.get('gameData', {}).get('weather', {})
        condition = weather_info.get('condition', 'N/A')
        temp = weather_info.get('temp', 'N/A')
        wind = weather_info.get('wind', 'N/A')
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Weather Condition", condition)
        col2.metric("Temperature", f"{temp}°F" if temp != 'N/A' else 'N/A')
        col3.metric("Wind", wind)
        
        st.markdown("---")
        
        # Display Lineups
        away_team_data = boxscore.get('away', {})
        home_team_data = boxscore.get('home', {})
        
        col_away, col_home = st.columns(2)
        
        with col_away:
            st.markdown(f"### ✈️ {away_team_data.get('team', {}).get('name', 'Away Team')} Lineup")
            away_batters = away_team_data.get('batters', [])
            if away_batters:
                away_lineup_rows = []
                for batter_id in away_batters:
                    player_info = away_team_data.get('players', {}).get(f"ID{batter_id}", {})
                    person = player_info.get('person', {})
                    position = player_info.get('position', {}).get('abbreviation', '')
                    away_lineup_rows.append({"Player": person.get('fullName', 'Unknown'), "Pos": position})
                st.dataframe(pd.DataFrame(away_lineup_rows), width='stretch', hide_index=True)
            else:
                st.info("Lineups not yet posted.")
                
        with col_home:
            st.markdown(f"### 🏠 {home_team_data.get('team', {}).get('name', 'Home Team')} Lineup")
            home_batters = home_team_data.get('batters', [])
            if home_batters:
                home_lineup_rows = []
                for batter_id in home_batters:
                    player_info = home_team_data.get('players', {}).get(f"ID{batter_id}", {})
                    person = player_info.get('person', {})
                    position = player_info.get('position', {}).get('abbreviation', '')
                    home_lineup_rows.append({"Player": person.get('fullName', 'Unknown'), "Pos": position})
                st.dataframe(pd.DataFrame(home_lineup_rows), width='stretch', hide_index=True)
            else:
                st.info("Lineups not yet posted.")
                
    except Exception as e:
        st.error(f"Could not load detailed boxscore/weather data for this game: {e}")

    st.markdown("---")
    st.subheader("📅 Full Slate Overview")
    
    matchup_list = []
    for game in games:
        matchup_list.append({
            "Game": f"{game['away_name']} @ {game['home_name']}",
            "Time": game.get('game_time', 'TBD'),
            "Venue": game.get('venue_name', 'Unknown'),
            "Status": game.get('status', 'Scheduled')
        })
    
    df_games = pd.DataFrame(matchup_list)
    st.dataframe(df_games, width='stretch')
