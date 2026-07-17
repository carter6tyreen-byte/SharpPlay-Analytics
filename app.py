import streamlit as st
import pandas as pd
import requests
import logging

# Set up logging for the optimizer
logging.basicConfig(level=logging.INFO)

# Path to the matchup data
DATA_URL = "https://raw.githubusercontent.com/carter6tyreen-byte/SharpPlay-Analytics/refs/heads/main/data/today_matchups.json"

def get_optimal_bets_with_sizing(predictions, market_odds):
    """Applies utility-based optimization and Kelly Criterion sizing."""
    try:
        df = pd.merge(predictions, market_odds, on='player_id', how='inner')
        df['implied_prob'] = 1 / df['decimal_odds']
        df['edge'] = df['prob'] - df['implied_prob']
        df['utility_score'] = df['edge'] * (1 - df['volatility'])
        df['b'] = df['decimal_odds'] - 1
        df['kelly_fraction'] = (df['b'] * df['prob'] - (1 - df['prob'])) / df['b']
        df['bet_size'] = df['kelly_fraction'].clip(0, 0.05)
        return df[df['utility_score'] > 0].copy()
    except Exception as e:
        logging.error(f"Error in starworld_optimizer: {e}")
        return pd.DataFrame()

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
            # 1. Fetch and Display Stats
            details = get_game_details(game_pk)
            away_players = details['teams']['away']['players']
            
            player_list = []
            for player_id, p_data in away_players.items():
                info = {
                    "player_id": player_id, # Required for optimizer join
                    "Name": p_data['person']['fullName'],
                    "Position": p_data.get('position', {}).get('abbreviation', 'N/A')
                }
                stats = p_data.get('stats', {})
                info.update(stats.get('batting', {}))
                info.update(stats.get('pitching', {}))
                player_list.append(info)
            
            df_stats = pd.DataFrame(player_list)
            df_clean = df_stats.reindex(columns=["Name", "Position", "atBats", "hits", "homeRuns", "strikeOuts", "baseOnBalls"]).dropna(subset=["Name"])
            df_active = df_clean[df_clean['atBats'] > 0] if 'atBats' in df_clean.columns else df_clean
            
            st.write("### Away Roster & Stats")
            st.dataframe(df_active, use_container_width=True, hide_index=True)

            # 2. Integrate Optimizer
            if st.button(f"Run Starworld Optimizer {game_pk}", key=f"opt_{game_pk}"):
                # Placeholder DataFrames - replace these with your actual model/market data sources
                # predictions = pd.read_csv("my_model_preds.csv")
                # market_odds = pd.read_csv("current_market_odds.csv")
                st.info("Optimizer run triggered. Ensure 'predictions' and 'market_odds' data sources are connected.")
