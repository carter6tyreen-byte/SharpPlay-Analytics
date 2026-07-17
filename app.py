import streamlit as st
from analytics.machine_engine import AnalyticsEngine

# Initialize the engine in session state so it persists
if 'engine' not in st.session_state:
    st.session_state.engine = AnalyticsEngine()

# Initialize a place to store analysis results
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

def main():
    st.title("MLB Analytics Board")
    
    st.header("Parlay Optimizer")
    parlay_players = ["Yordan Alvarez", "Hunter Goodman", "Ben Rice", "Eduardo Valencia"]
    
    # Create buttons
    cols = st.columns(len(parlay_players))
    for i, player in enumerate(parlay_players):
        if cols[i].button(f"Analyze {player.split()[-1]}"):
            with st.spinner(f'Optimizing {player}...'):
                # Call your engine
                st.session_state.analysis_results = st.session_state.engine.run_starworld_optimizer(player)
                st.session_state.current_player = player

    # Display results if they exist in session state
    if st.session_state.analysis_results is not None:
        st.write(f"### Results for {st.session_state.current_player}")
        st.dataframe(st.session_state.analysis_results)
