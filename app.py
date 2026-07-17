import streamlit as st
import pandas as pd
from analytics.machine_engine import AnalyticsEngine

# Set page layout once
st.set_page_config(layout="wide")

def main():
    # Initialize the engine
    engine = AnalyticsEngine()
    
    st.title("SharpPLAY Value Board")
    
    # Initialize session state for navigation
    if 'selected_game' not in st.session_state:
        st.session_state.selected_game = None
        
    if st.session_state.selected_game is None:
        st.write("### Today's Matchups")
        
        # Corrected: Handle potential None or empty DataFrames safely
        games_df = engine.get_all_games()
        
        if games_df is None or games_df.empty:
            st.warning("No games found.")
        else:
            for _, row in games_df.iterrows():
                if st.button(f"{row['Game']}", key=row['GameID']):
                    st.session_state.selected_game = row['GameID']
                    st.rerun()
    else:
        # Navigation back button
        if st.button("← Back to Matchups"):
            st.session_state.selected_game = None
            st.rerun()
            
        st.write(f"### Live Roster for: {st.session_state.selected_game}")
        
        # Fetch roster data using the optimizer method
        player_df = engine.run_starworld_optimizer(st.session_state.selected_game)
        
        def highlight_status(val):
            return 'background-color: lightgreen' if val == 'Active' else 'background-color: lightgrey'
            
        if player_df is not None and not player_df.empty:
            if 'Status' in player_df.columns:
                st.dataframe(player_df.style.map(highlight_status, subset=['Status']), use_container_width=True)
            else:
                st.dataframe(player_df, use_container_width=True)
        else:
            st.error("No roster data available for this game.")

if __name__ == "__main__":
    main()
