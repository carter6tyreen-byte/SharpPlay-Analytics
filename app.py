import streamlit as st
# Assuming your engine is in a file named machine_engine.py
from machine_engine import AnalyticsEngine 

def main():
    st.title("SharpPLAY Value Board")

    # 1. Define game_id BEFORE using it
    # You can set a default or allow user input
    game_id = st.text_input("Enter Game ID", value="823440")

    # 2. Initialize the engine
    # Initialize outside the button to avoid re-instantiation issues
    engine = AnalyticsEngine()

    # 3. Handle the button click
    # game_id is now defined and ready to be used
    if st.button(f"Run Starworld Optimizer {game_id}"):
        try:
            with st.spinner('Calculating value...'):
                # Call your optimizer method
                results = engine.run_starworld_optimizer(game_id=game_id)
                
                # Display the results
                st.write("### Optimization Results")
                st.dataframe(results)
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
