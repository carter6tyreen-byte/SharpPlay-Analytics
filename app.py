import streamlit as st
import pandas as pd
from analytics.machine_engine import AnalyticsEngine

# Set layout to wide
st.set_page_config(layout="wide")

def main():
    st.title("SharpPLAY Value Board")
    
    # Initialize engine
    engine = AnalyticsEngine()
    
    # Navigation state
    if 'selected_game' not in st.session_state:
        st.session_state.selected_game = None

    # Home Screen
    if st.session_state.selected_game is None:
        st.write("### Today's Matchups")
        games_df = engine.get_all_games()
        
        if games_df.empty:
            st.warning("No games found. Check your data collector.")
        else:
            for _, row in games_df.iterrows():
                if st.button(f"View {row['Game']}", key=row['GameID']):
                    st.session_state.selected_game = row['GameID']
                    st.rerun()
    
    # Detail Screen
    else:
        if st.button("← Back to Matchups"):
            st.session_state.selected_game = None
            st.rerun()
            
        st.write(f"### Live Roster for Game: {st.session_state.selected_game}")
        player_df = engine.run_starworld_optimizer(st.session_state.selected_game)
        
        # Style function for Status column
        def highlight_status(val):
            return 'background-color: lightgreen' if val == 'Active' else 'background-color: lightgrey'

        # Use .map() to avoid AttributeError
        if 'Status' in player_df.columns:
            st.dataframe(
                player_df.style.map(highlight_status, subset=['Status']),
                use_container_width=True
            )
        else:
            st.dataframe(player_df, use_container_width=True)

if __name__ == "__main__":
    main()
