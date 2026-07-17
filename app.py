import streamlit as st
from analytics.matchup_engine import AnalyticsEngine

# Initialize Engine
engine = AnalyticsEngine(raw_data={})

def color_grading(val):
    """Helper for color-coding 80/80/80 criteria."""
    color = 'green' if val >= 80 else 'red'
    return f'color: {color}'

# Dashboard UI for a specific game
if st.button(f"Run Starworld Optimizer {game_id}"):
    # Fetch processed data
    df = engine.run_starworld_optimizer(game_id)
    
    if not df.empty:
        # Display the table with styling
        st.dataframe(
            df.style.applymap(
                color_grading, 
                subset=['metric_1', 'metric_2', 'metric_3']
            )
        )
    else:
        st.error("No data found for this game. Check your API connection.")
