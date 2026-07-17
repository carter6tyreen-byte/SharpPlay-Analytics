import streamlit as st
from analytics.matchup_engine import AnalyticsEngine

def color_grading(val):
    """Green for >= 80, Red otherwise."""
    color = 'green' if isinstance(val, (int, float)) and val >= 80 else 'red'
    return f'color: {color}'

# Inside your dashboard game loop:
if st.button(f"Run Starworld Optimizer {game_id}"):
    # Instantiate engine only when the button is clicked
    engine = AnalyticsEngine() 
    df = engine.run_starworld_optimizer(game_id)
    
    if not df.empty:
        # Apply formatting to numeric columns
        styled_df = df.style.applymap(
            color_grading, 
            subset=['metric_1', 'metric_2', 'metric_3']
        )
        st.dataframe(styled_df)
    else:
        st.warning("Optimizer returned no data.")
