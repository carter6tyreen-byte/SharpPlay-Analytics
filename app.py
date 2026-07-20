import streamlit as st
import statsapi
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(page_title="SharpPlay Analytics - MLB Matchups", layout="wide")

st.title("⚾ SharpPlay Analytics: Matchups, Lineups & Pitcher vs. Batter")

# Date configuration sidebar with a submit/search button
today_str = datetime.now().strftime("%m/%d/%Y")
st.sidebar.header("Configuration")
date_input = st.sidebar.text_input("Query Date (MM/DD/YYYY)", value=today_str)

# Search button so mobile users can trigger updates cleanly after typing
search_clicked = st.sidebar.button("Search Date", type="primary")

# Persist the selected date in session state to handle re-runs
if "selected_date" not in st.session_state:
    st.session_state.selected_date = today_str

if search_clicked:
    st.session_state.selected_date = date_input

selected_date = st.session_state.selected_date

@st.cache_data
def fetch_mlb_schedule(date_str):
    try:
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
    
    st.subheader("📋 Game Details, Weather, Lineups & Pitcher vs. Batter")
    
    game_options = {f"{g['away_name']} @ {g['home_name']} ({g.get('game_time', 'TBD')}) - ID: {g['game_id']}": g['game_id'] for g in games}
    selected_game_label = st.selectbox("Select a Matchup to View Details", options=list(game_options.keys()))
    selected_game_id = game_options[selected_game_label]
    
    try:
        boxscore = statsapi.boxscore_data(selected_game_id)
        game_status_data = statsapi.get("game", {"gamePk": selected_game_id})
        
        # Weather info
        weather_info = game_status_data.get('gameData', {}).get('weather', {})
        condition = weather_info.get('condition', 'N/A')
        temp = weather_info.get('temp', 'N/A')
        wind = weather_info.get('wind', 'N/A')
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Weather Condition", condition)
        col2.metric("Temperature", f"{temp}°F" if temp != 'N/A' else 'N/A')
        col3.metric("Wind", wind)
        
        st.markdown("---")
        
        away_team_data = boxscore.get('away', {})
        home_team_data = boxscore.get('home', {})
        
        away_pitchers = away_team_data.get('pitchers', [])
        home_pitchers = home_team_data.get('pitchers', [])
        
        away_sp_id = away_pitchers[0] if away_pitchers else None
        home_sp_id = home_pitchers[0] if home_pitchers else None
        
        away_sp_name = away_team_data.get('players', {}).get(f"ID{away_sp_id}", {}).get('person', {}).get('fullName', 'Away Starting Pitcher') if away_sp_id else 'Unknown'
        home_sp_name = home_team_data.get('players', {}).get(f"ID{home_sp_id}", {}).get('person', {}).get('fullName', 'Home Starting Pitcher') if home_sp_id else 'Unknown'

        col_away, col_home = st.columns(2)
        
        with col_away:
            st.markdown(f"### ✈️ {away_team_data.get('team', {}).get('name', 'Away Team')} Lineup")
            st.caption(f"vs. Opposing Pitcher: **{home_sp_name}**")
            away_batters = away_team_data.get('batters', [])
            
            if away_batters:
                away_lineup_rows = []
                for batter_id in away_batters:
                    player_info = away_team_data.get('players', {}).get(f"ID{batter_id}", {})
                    person = player_info.get('person', {})
                    position = player_info.get('position', {}).get('abbreviation', '')
                    batter_name = person.get('fullName', 'Unknown')
                    away_lineup_rows.append({"Player": batter_name, "Pos": position})
                    
                st.dataframe(pd.DataFrame(away_lineup_rows), width='stretch', hide_index=True)
            else:
                st.info("Lineups not yet posted.")
                
        with col_home:
            st.markdown(f"### 🏠 {home_team_data.get('team', {}).get('name', 'Home Team')} Lineup")
            st.caption(f"vs. Opposing Pitcher: **{away_sp_name}**")
            home_batters = home_team_data.get('batters', [])
            
            if home_batters:
                home_lineup_rows = []
                for batter_id in home_batters:
                    player_info = home_team_data.get('players', {}).get(f"ID{batter_id}", {})
                    person = player_info.get('person', {})
                    position = player_info.get('position', {}).get('abbreviation', '')
                    batter_name = person.get('fullName', 'Unknown')
                    home_lineup_rows.append({"Player": batter_name, "Pos": position})
                    
                st.dataframe(pd.DataFrame(home_lineup_rows), width='stretch', hide_index=True)
            else:
                st.info("Lineups not yet posted.")
                
    except Exception as e:
        st.error(f"Could not load boxscore data: {e}")

    st.markdown("---")
    st.subheader("📅 Full Slate Overview")
    
    matchup_list = []
    for game in games:
        raw_time = game.get('game_datetime') or game.get('game_time', 'TBD')
        if 'T' in str(raw_time):
            try:
                dt_obj = datetime.strptime(raw_time[:19], "%Y-%m-%dT%H:%M:%S")
                formatted_time = dt_obj.strftime("%I:%M %p ET")
            except Exception:
                formatted_time = raw_time
        else:
            formatted_time = raw_time

        matchup_list.append({
            "Game": f"{game['away_name']} @ {game['home_name']}",
            "Time": formatted_time,
            "Venue": game.get('venue_name', 'Unknown'),
            "Status": game.get('status', 'Scheduled')
        })
    
    df_games = pd.DataFrame(matchup_list)
    st.dataframe(df_games, width='stretch')
