import streamlit as st
import pandas as pd
from analytics.machine_engine import AnalyticsEngine

def main():
    st.title("MLB Analytics Board")
    
    engine = AnalyticsEngine()
    df = engine.get_all_games()
    
    # 1. Validation: Ensure the data contains the expected 'games' list
    if df.empty or 'games' not in df.columns:
        st.write("No schedule data found.")
        return

    # 2. Unpacking: The API nests games inside a list for each date
    # We take the first available date entry
    games_list = df.iloc[0].get('games', [])
    
    if not games_list:
        st.write("No games scheduled for this date.")
        return

    # 3. Processing: Convert the nested list into a usable DataFrame
    games_df = pd.DataFrame(games_list)

    # 4. Rendering: Iterate through the unpacked games
    for index, row in games_df.iterrows():
        try:
            # Path: teams -> away/home -> team -> name
            away = row['teams']['away']['team']['name']
            home = row['teams']['home']['team']['name']
            game_id = str(row['gamePk'])
            
            label = f"{away} @ {home}"
            
            # Using gamePk as a unique key for the button
            if st.button(f"Analyze: {label}", key=game_id):
                with st.spinner('Running Optimizer...'):
                    results = engine.run_starworld_optimizer(game_id)
                    st.dataframe(results)
        except KeyError as e:
            st.error(f"Data mapping error: Missing field {e}")
            continue

if __name__ == "__main__":
    main()
