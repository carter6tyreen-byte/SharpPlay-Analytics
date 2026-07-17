import streamlit as st
import pandas as pd
import requests

DATA_URL = "https://raw.githubusercontent.com/carter6tyreen-byte/SharpPlay-Analytics/refs/heads/main/data/today_matchups.json"

@st.cache_data(ttl=3600)
def load_schedule():
    response = requests.get(DATA_URL)
    data = response.json()
    return data.get("dates", [{}])[0].get("games", [])

def get_game_details(game_pk):
    url = f"https://statsapi.mlb.com/api/v1/game/{game_pk}/boxscore"
    return requests.get(url).json()

st.set_page_config(page_title="SharpPLAY Analytics", layout="wide")
st.title("⚾ SharpPLAY Analytics Dashboard")

games = load_schedule()
df_games = pd.json_normalize(games)

for index, row in df_games.iterrows():
    game_pk = row['gamePk']
    away_team = row['teams.away.team.name']
    home_team = row['teams.home.team.name']
    
    with st.expander(f"{away_team} @ {home_team}"):
        if st.button(f"Load Full Stats for Game {game_pk}", key=f"btn_{game_pk}"):
            with st.spinner("Fetching player stats..."):
                details = get_game_details(game_pk)
                away_players = details['teams']['away']['players']
                
                player_list = []
                for player_id, p_data in away_players.items():
                    # Extract basic info
                    info = {
                        "Name": p_data['person']['fullName'],
                        "Position": p_data.get('position', {}).get('abbreviation', 'N/A')
                    }
                    
                    # Extract stats if they exist
                    stats = p_data.get('stats', {})
                    # Add batting stats (e.g., avg, homeRuns)
                    info.update(stats.get('batting', {}))
                    # Add pitching stats (e.g., era, strikeOuts)
                    info.update(stats.get('pitching', {}))
                    
                    player_list.append(info)
                
                st.write("### Away Roster & Stats")
                # Create DataFrame and clean up empty columns
                df_stats = pd.DataFrame(player_list)
                st.dataframe(df_stats, use_container_width=True, hide_index=True)

if not games:
    st.warning("No games found.")
