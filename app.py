import streamlit as st
import pandas as pd
from analytics.machine_engine import AnalyticsEngine

def main():
    st.title("MLB Analytics Board")
    
    engine = AnalyticsEngine()
    df = engine.get_all_games()
    
    # Check if df is empty
    if df.empty:
        st.write("No games found.")
        return

    # DEBUG: See what your data actually looks like
    # st.write("Available columns:", df.columns.tolist())

    # Ensure your column names match the strings below exactly
    # For this example, I am using common MLB API keys
    # Adjust these strings to match the output of st.write(df.columns)
    display_col = 'game_label'  # e.g., 'NYY vs BOS'
    id_col = 'gamePk'           # e.g., the unique ID for the game

    if display_col not in df.columns or id_col not in df.columns:
        st.error(f"Data error: Looking for '{display_col}' and '{id_col}', but columns are {df.columns.tolist()}")
        return

    for index, row in df.iterrows():
        # Using a unique key based on the GameID to prevent Streamlit button errors
        if st.button(f"Analyze: {row[display_col]}", key=str(row[id_col])):
            st.write(f"Loading data for game: {row[id_col]}")
            # Your optimizer logic
            results = engine.run_starworld_optimizer(row[id_col])
            st.dataframe(results)

if __name__ == "__main__":
    main()
