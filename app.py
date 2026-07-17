streamlit run app.py⁠
import streamlit as st
import pandas as pd

# Initialize session state for drill-down navigation
if 'selected_game' not in st.session_state:
    st.session_state.selected_game = None

def main():
    st.title("SharpPLAY Value Board")
    
    # Load your data
    engine = AnalyticsEngine() 
    
    if st.session_state.selected_game is None:
        # Show all games
        games_df = engine.get_all_games() # Your method to list all matchups
        st.write("### Today's Matchups")
        for index, row in games_df.iterrows():
            if st.button(f"View {row['Game']}", key=row['GameID']):
                st.session_state.selected_game = row['GameID']
                st.rerun()
    else:
        # Show player optimization for the selected game
        if st.button("← Back to Matchups"):
            st.session_state.selected_game = None
            st.rerun()
            
        st.write(f"### Optimization for Game: {st.session_state.selected_game}")
        player_df = engine.run_starworld_optimizer(st.session_state.selected_game)
        st.dataframe(player_df) # Interactive table for player data
