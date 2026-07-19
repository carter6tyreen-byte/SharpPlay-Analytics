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
    color = 'green' if isinstance(val, (int, float)) and val < 3.5 else 'black'
    return f'color: {color}'

def style_batter_hr(val):
    color = 'green' if isinstance(val, (int, float)) and val > 30 else 'black'
    return f'color: {color}'

# --- Pitcher Section ---
st.subheader("Pitcher ERA Leaders")
# Note: Ensure get_pitcher_data in your engine is updated to use order='asc'
pitcher_df = engine.get_pitcher_data()
if pitcher_df is not None and not pitcher_df.empty:
    styled_pitcher = pitcher_df.style.map(style_pitcher_era, subset=['Value'])
    # FIX: Using 'stretch' to fill container correctly
    st.dataframe(styled_pitcher, width='stretch') 
else:
    st.warning("No pitcher data available.")

# --- Batter Section ---
st.subheader("Batter Home Run Leaders")
batter_df = engine.get_batter_data()
if batter_df is not None and not batter_df.empty:
    styled_batter = batter_df.style.map(style_batter_hr, subset=['Value'])
    # FIX: Using 'stretch' to fill container correctly
    st.dataframe(styled_batter, width='stretch')
else:
    st.warning("No batter data available.")
