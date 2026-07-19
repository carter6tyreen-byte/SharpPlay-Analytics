import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="SharpPlay Analytics: ODE Optimizer", layout="wide")

st.title("SharpPlay Analytics: ODE Optimizer")

DISTRIBUTIONS_PATH = "data/player_distributions.json"
AUDIT_PATH = "data/audit_results.json"

player_data = None
if os.path.exists(DISTRIBUTIONS_PATH):
    try:
        with open(DISTRIBUTIONS_PATH, "r") as f:
            content = f.read().strip()
            if content:
                player_data = json.loads(content)
    except Exception as e:
        st.error(f"Error parsing JSON: {e}")

if player_data:
    st.success("Player distributions successfully loaded!")
    st.subheader("Player Performance Distributions")
    df_dist = pd.DataFrame.from_dict(player_data, orient='index')
    st.dataframe(df_dist, use_container_width=True)
else:
    st.warning("⚠️ Could not fetch data from GitHub raw URL yet.")
    st.info("Check if your GitHub Action has successfully completed and pushed data/player_distributions.json to the main branch.")

if os.path.exists(AUDIT_PATH):
    st.subheader("Audit & Model Accuracy Loop")
    try:
        with open(AUDIT_PATH, "r") as f:
            audit_content = f.read().strip()
            if audit_content:
                audit_data = json.loads(audit_content)
                if audit_data:
                    st.dataframe(pd.DataFrame(audit_data), use_container_width=True)
    except Exception as e:
        st.warning(f"Could not load audit results: {e}")

if st.button("Force Refresh"):
    st.rerun()
