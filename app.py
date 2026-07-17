import streamlit as st
import pandas as pd
from analytics.machine_engine import AnalyticsEngine

st.set_page_config(page_title="MLB Analytics Board", layout="wide")

# Initialize engine
engine = AnalyticsEngine()

st.title("MLB Daily Analytics")

# Create two tabs
tab1, tab2 = st.tabs(["Pitcher Dashboard", "Batter Dashboard"])

with tab1:
    st.subheader("Pitcher Performance")
    pitcher_df = engine.get_pitcher_data()
    st.dataframe(pitcher_df, use_container_width=True)

with tab2:
    st.subheader("Batter Performance")
    batter_df = engine.get_batter_data()
    st.dataframe(batter_df, use_container_width=True)
