import streamlit as st
import pandas as pd
from analytics.machine_engine import AnalyticsEngine

# Set page to wide mode for better table viewing
st.set_page_config(layout="wide")

def main():
    st.title("SharpPLAY Value Board")
    
    engine = AnalyticsEngine()
    
    # Session state for navigation
    if 'selected_game' not in st.session_state:
        st.session_state.selected_game = None

    if st.session_state.selected_game is None:
        st.write("### Today's Matchups")
        games_df = engine.get_all_games()
        
        # Display as a grid of buttons
        for _, row in games_df.iterrows():
            if st.button(f"View {row['Game']}", key=row['GameID']):
                st.session_state.selected_game = row['GameID']
                st.rerun()
    else:
        # Navigation
        if st.button("← Back to Matchups"):
            st.session_state.selected_game = None
            st.rerun()
            
        st.write(f"### Live Roster & Metrics for Game: {st.session_state.selected_game}")
        
        # Get data
        player_df = engine.run_starworld_optimizer(st.session_state.selected_game)
        
        # Apply Heatmap Styling (Example: color-coding status)
        # Note: You can expand this to style numeric columns as you add them
        def highlight_status(val):
            color = 'lightgreen' if val == 'Active' else 'lightgrey'
            return f'background-color: {color}'

        st.dataframe(
            player_df.style.applymap(highlight_status, subset=['Status']),
            use_container_width=True
        )

if __name__ == "__main__":
    main()
