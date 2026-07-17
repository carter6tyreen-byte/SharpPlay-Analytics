import streamlit as st
import pandas as pd
from analytics.machine_engine import AnalyticsEngine

# Initialize session state for drill-down navigation
if 'selected_game' not in st.session_state:
    st.session_state.selected_game = None

def main():
    st.title("SharpPLAY Value Board")
    
    engine = AnalyticsEngine() 
    
    if st.session_state.selected_game is None:
        games_df = engine.get_all_games()
        st.write("### Today's Matchups")
        for _, row in games_df.iterrows():
            if st.button(f"View {row['Game']}", key=row['GameID']):
                st.session_state.selected_game = row['GameID']
                st.rerun()
    else:
        if st.button("← Back to Matchups"):
            st.session_state.selected_game = None
            st.rerun()
            
        st.write(f"### Optimization for Game: {st.session_state.selected_game}")
        player_df = engine.run_starworld_optimizer(st.session_state.selected_game)
        st.dataframe(player_df)

if __name__ == "__main__":
    main()
