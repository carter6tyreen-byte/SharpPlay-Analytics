import streamlit as st
import sys
import os

# FIX: Add the current directory to sys.path to ensure 'analytics' is found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Now import the engine
from analytics.machine_engine import AnalyticsEngine

def main():
    st.title("SharpPLAY Value Board")

    # Define game_id
    game_id = st.text_input("Enter Game ID", value="823440")

    # Initialize the engine
    try:
        engine = AnalyticsEngine()
    except Exception as e:
        st.error(f"Error initializing engine: {e}")
        return

    if st.button(f"Run Starworld Optimizer {game_id}"):
        try:
            with st.spinner('Calculating value...'):
                results = engine.run_starworld_optimizer(game_id=game_id)
                st.write("### Optimization Results")
                st.dataframe(results)
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
