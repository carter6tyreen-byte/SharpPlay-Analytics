import streamlit as st
import pandas as pd
from analytics.machine_engine import AnalyticsEngine

def main():
    st.title("MLB Analytics Board")
    
    engine = AnalyticsEngine()
    df = engine.get_all_games()
    
    if df.empty or 'games' not in df.columns:
        st.write("No schedule data found.")
        return

    # Unpack games from the API data
    games_list = df.iloc[0].get('games', [])
    games_df = pd.DataFrame(games_list)

    # PARLAY ANALYSIS SECTION
    st.divider()
    st.header("Parlay Optimizer")
    parlay_players = ["Yordan Alvarez", "Hunter Goodman", "Ben Rice", "Eduardo Valencia"]
    
    # Create columns for clean UI
    cols = st.columns(len(parlay_players))
    for i, player in enumerate(parlay_players):
        with cols[i]:
            if st.button(f"Analyze {player.split()[-1]}"):
                with st.spinner(f'Optimizing {player}...'):
                    # The engine uses the game ID to get data; 
                    # Assuming you can lookup gamePk via player name in your engine
                    results = engine.run_starworld_optimizer(player)
                    st.write(f"**{player}**")
                    st.dataframe(results)
    st.divider()

    # ORIGINAL GAME LISTING
    st.header("Full Schedule")
    for index, row in games_df.iterrows():
        try:
            away = row['teams']['away']['team']['name']
            home = row['teams']['home']['team']['name']
            game_id = str(row['gamePk'])
            
            if st.button(f"Analyze: {away} @ {home}", key=game_id):
                with st.spinner('Running Optimizer...'):
                    results = engine.run_starworld_optimizer(game_id)
                    st.dataframe(results)
        except KeyError:
            continue

if __name__ == "__main__":
    main()
