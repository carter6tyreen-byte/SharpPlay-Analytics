import streamlit as st
from analytics.machine_engine import AnalyticsEngine

st.set_page_config(page_title="MLB Analytics Board", layout="wide")
st.title("MLB Analytics Board")

engine = AnalyticsEngine()

st.subheader("Pitcher ERA Leaders")
pitcher_df = engine.get_pitcher_data()
if pitcher_df is not None and not pitcher_df.empty:
    st.dataframe(pitcher_df, use_container_width=True)
else:
    st.warning("No pitcher data available.")

st.subheader("Batter Home Run Leaders")
batter_df = engine.get_batter_data()
if batter_df is not None and not batter_df.empty:
    st.dataframe(batter_df, use_container_width=True)
else:
    st.warning("No batter data available.")
