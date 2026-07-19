import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="SharpPlay Analytics: ODE Optimizer", layout="wide")

st.title("SharpPlay Analytics: ODE Optimizer")

DISTRIBUTIONS_PATH = "data/player_distributions.json"
AUDIT_PATH = "data/audit_results.json"

if os.path.exists(DISTRIBUTIONS_PATH):
    try:
        with open(DISTRIBUTIONS_PATH, "r") as f:
            player_data = json.load(f)
            if player_data:
                st.success("Player distributions successfully loaded!")
                st.subheader("Player Performance Distributions")
                df_dist = pd.DataFrame.from_dict(player_data, orient='index')
                st.dataframe(df_dist, use_container_width=True)
            else:
                st.warning("⚠️ player_distributions.json file is currently empty.")
    except Exception as e:
        st.error(f"Error parsing JSON file: {e}")
else:
    st.error("❌ player_distributions.json not found in the data directory.")

if os.path.exists(AUDIT_PATH):
    try:
        with open(AUDIT_PATH, "r") as f:
            audit_data = json.load(f)
            if audit_data:
                st.subheader("Audit & Model Accuracy Loop")
                st.dataframe(pd.DataFrame(audit_data), use_container_width=True)
    except Exception as e:
        st.warning(f"Could not load audit results: {e}")

if st.button("Force Refresh"):
    st.rerun()
