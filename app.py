import streamlit as st
from analytics.machine_engine import AnalyticsEngine

if 'engine' not in st.session_state:
    try:
        st.session_state.engine = AnalyticsEngine()
    except Exception as e:
        st.error(f"Failed to initialize AnalyticsEngine: {e}")
        st.stop()

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

def main():
    st.title("MLB Analytics Board")
    
    st.header("Parlay Optimizer")
    parlay_players = ["Yordan Alvarez", "Hunter Goodman", "Ben Rice", "Eduardo Valencia"]
    
    cols = st.columns(len(parlay_players))
    for i, player in enumerate(parlay_players):
        if cols[i].button(f"Analyze {player.split()[-1]}"):
            with st.spinner(f'Optimizing {player}...'):
                try:
                    # Capture result and handle potential errors
                    results = st.session_state.engine.run_starworld_optimizer(player)
                    st.session_state.analysis_results = results
                    st.session_state.current_player = player
                except Exception as e:
                    st.error(f"Error running optimizer for {player}: {e}")
                    st.session_state.analysis_results = None

    if st.session_state.analysis_results is not None:
        st.write(f"### Results for {st.session_state.current_player}")
        st.dataframe(st.session_state.analysis_results)

if __name__ == "__main__":
    main()
