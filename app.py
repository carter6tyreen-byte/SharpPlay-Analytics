import streamlit as st
import json
import os

DIST_FILE = 'data/player_distributions.json'

def load_distributions():
    if not os.path.exists(DIST_FILE):
        return None
    with open(DIST_FILE, 'r') as f:
        return json.load(f)

st.title("SharpPlay Analytics: ODE Optimizer")

dist_data = load_distributions()

if dist_data is None:
    st.warning("Data is processing. Please check the GitHub Actions tab.")
    if st.button("Check for Data"):
        st.rerun()
else:
    player = st.selectbox("Select Hitter", list(dist_data.keys()))
    if player:
        st.write(f"### {player} Analysis")
        st.json(dist_data[player])
