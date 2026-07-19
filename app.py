import streamlit as st
from analytics.machine_engine import AnalyticsEngine

# Set page layout
st.set_page_config(page_title="MLB Analytics Board", layout="wide")
st.title("MLB Analytics Board")

@st.cache_resource
def get_engine():
    return AnalyticsEngine()

engine = get_engine()

# Styling functions
def style_pitcher_era(val):
    # For ERA, lower is better (green). If value is 0 or invalid, color black.
    color = 'green' if isinstance(val, (int, float)) and val < 3.5 else 'black'
    return f'color: {color}'

def style_batter_hr(val):
    # For HR, higher is better (green).
    color = 'green' if isinstance(val, (int, float)) and val > 30 else 'black'
    return f'color: {color}'

# --- Pitcher Section ---
st.subheader("Pitcher ERA Leaders")
pitcher_df = engine.get_pitcher_data()
if pitcher_df is not None and not pitcher_df.empty:
    # Use .map() for styling
    styled_pitcher = pitcher_df.style.map(style_pitcher_era, subset=['Value'])
    st.dataframe(styled_pitcher, use_container_width=True)
else:
    st.warning("No pitcher data available.")

# --- Batter Section ---
st.subheader("Batter Home Run Leaders")
batter_df = engine.get_batter_data()
if batter_df is not None and not batter_df.empty:
    # Use .map() for styling
    styled_batter = batter_df.style.map(style_batter_hr, subset=['Value'])
    st.dataframe(styled_batter, use_container_width=True)
else:
    st.warning("No batter data available.")
