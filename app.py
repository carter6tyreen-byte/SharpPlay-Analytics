import streamlit as st
from analytics.machine_engine import AnalyticsEngine

# 1. Page Configuration
st.set_page_config(page_title="MLB Analytics Board", layout="wide")

# 2. Initialize Session State
if 'engine' not in st.session_state:
    try:
        st.session_state.engine = AnalyticsEngine()
    except Exception as e:
        st.error(f"Engine initialization error: {e}")
        st.stop()

if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'current_player' not in st.session_state:
    st.session_state.current_player = None

# 3. Main Logic
def main():
    st.title("MLB Analytics Board")
    
    st.header("Parlay Optimizer")
    parlay_players = ["Yordan Alvarez", "Hunter Goodman", "Ben Rice", "Eduardo Valencia"]
    
    # Create columns for buttons
    cols = st.columns(len(parlay_players))
    for i, player in enumerate(parlay_players):
        # Using the last name for the button label
        if cols[i].button(f"Analyze {player.split()[-1]}"):
            with st.spinner(f'Optimizing {player}...'):
                try:
                    # Run the engine
                    results = st.session_state.engine.run_starworld_optimizer(player)
                    # Update session state to persist data
                    st.session_state.analysis_results = results
                    st.session_state.current_player = player
                except Exception as e:
                    st.error(f"Error running optimizer for {player}: {e}")
                    st.session_state.analysis_results = None

    # 4. Display Logic
    if st.session_state.analysis_results is not None:
        st.write("---")
        st.write(f"### Results for {st.session_state.current_player}")
        st.dataframe(st.session_state.analysis_results, use_container_width=True)
    else:
        st.info("Select a player above to run the simulation.")

if __name__ == "__main__":
    main()
