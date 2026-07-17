import streamlit as st
import pandas as pd
from analytics.machine_engine import AnalyticsEngine

def main():
    st.title("MLB Analytics Board")
    
    engine = AnalyticsEngine()
    df = engine.get_all_games()
    
    # 1. DEBUG: Uncomment the next line to see your true column names
    # st.write("Available columns:", df.columns.tolist())
    
    if df.empty:
        st.write("No games found.")
        return

    # 2. FIX: Replace these strings with the actual names from the debug output
    # For example: display_col = 'away_name' and id_col = 'gamePk'
    display_col = 'actual_display_column_name' 
    id_col = 'actual_id_column_name'           

    # 3. SAFETY: Check if columns exist before looping
    if display_col not in df.columns or id_col not in df.columns:
        st.error(f"Error: Columns '{display_col}' or '{id_col}' not found. Available: {df.columns.tolist()}")
        return

    # 4. LOOP: Safely iterate and create unique buttons
    for index, row in df.iterrows():
        # Ensure the key is converted to a string to avoid hash collisions
        button_label = f"Analyze: {row[display_col]}"
        button_key = str(row[id_col])
        
        if st.button(button_label, key=button_key):
            with st.spinner('Running Optimizer...'):
                results = engine.run_starworld_optimizer(row[id_col])
                st.dataframe(results)

if __name__ == "__main__":
    main()

