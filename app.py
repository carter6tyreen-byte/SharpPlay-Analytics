import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="SharpPlay Analytics: ODE Optimizer", layout="wide")

st.title("SharpPlay Analytics: ODE Optimizer")

# Debugging section to see what directory the app is currently running in
with st.expander("🛠️ Environment Debugger"):
    st.write("Current Working Directory:", os.getcwd())
    st.write("Files in root:", os.listdir('.'))
    if os.path.exists('data'):
        st.write("Files in 'data' directory:", os.listdir('data'))
    else:
        st.error("'data' directory not found by Streamlit container!")

DISTRIBUTIONS_PATH = os.path.join("data", "player_distributions.json")
AUDIT_PATH = os.path.join("data", "audit_results.json")

# Attempt to load data directly without hard-stopping
player_data = None
if os.path.exists(DISTRIBUTIONS_PATH):
    try:
        with open(DISTRIBUTIONS_PATH, "r") as f:
            player_data = json.load(f)
    except Exception as e:
        st.error(f"Error parsing JSON: {e}")

if player_data:
    st.success("Data successfully loaded!")
    st.subheader("Player Performance Distributions")
    df_dist = pd.DataFrame.from_dict(player_data, orient='index')
    st.dataframe(df_dist, use_container_width=True)
else:
    st.warning("⚠️ player_distributions.json not detected in the Streamlit container yet.")
    st.info("Try going to your Streamlit Community Cloud dashboard, click the 3 dots next to your app, and select **Clear cache & reboot**.")

# Optional: Audit Results Section
if os.path.exists(AUDIT_PATH):
    st.subheader("Audit & Model Accuracy Loop")
    try:
        with open(AUDIT_PATH, "r") as f:
            audit_data = json.load(f)
            if audit_data:
                st.dataframe(pd.DataFrame(audit_data), use_container_width=True)
    except Exception as e:
        st.warning(f"Could not load audit results: {e}")

if st.button("Force Refresh"):
    st.rerun()
