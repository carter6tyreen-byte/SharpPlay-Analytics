import streamlit as st
import pandas as pd
from analytics.machine_engine import AnalyticsEngine

# Page config must be at the top level with no indentation
st.set_page_config(page_title="MLB Analytics Board", layout="wide")


# 2. Initialize Session State
if 'engine' not in st.session_state:
    st.session_state.engine = AnalyticsEngine()
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'current_player' not in st.session_state:
    st.session_state.current_player = None

# 3. Main Logic
def main():
    st.title("MLB Analytics Board")
    
    st.header("Parlay Optimizer")
    parlay_players = ["Yordan Alvarez", "Hunter Goodman", "Ben Rice", "Eduardo Valencia"]
    
    cols = st.columns(len(parlay_players))
    for i, player in enumerate(parlay_players):
        if cols[i].button(f"Analyze {player.split()[-1]}"):
            with st.spinner(f'Optimizing {player}...'):
                try:
                    results = st.session_state.engine.run_starworld_optimizer(player)
                    st.session_state.analysis_results = results
                    st.session_state.current_player = player
                except Exception as e:
                    st.error(f"Error: {e}")
                    st.session_state.analysis_results = None

    # 4. Corrected Display Logic
    if st.session_state.analysis_results is not None:
        st.write("---")
        st.write(f"### Results for {st.session_state.current_player}")
        
        # Ensure we are handling the data type correctly
        if isinstance(st.session_state.analysis_results, pd.DataFrame):
            if not st.session_state.analysis_results.empty:
                st.dataframe(st.session_state.analysis_results, use_container_width=True)
            else:
                st.warning("The engine returned an empty dataset.")
        else:
            # Fallback for non-DataFrame results (lists/dicts)
            st.write("Raw Output:", st.session_state.analysis_results)
    else:
        st.info("Select a player above to run the simulation.")

if __name__ == "__main__":
    main()
