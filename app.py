import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="SharpPlay Analytics: ODE Optimizer", layout="wide")

st.title("SharpPlay Analytics: ODE Optimizer")

# Define file paths safely using flat directory structure
DISTRIBUTIONS_PATH = os.path.join("data", "player_distributions.json")
AUDIT_PATH = os.path.join("data", "audit_results.json")
METRICS_PATH = os.path.join("data", "master_player_metrics.csv")

# Function to check data availability
def check_data():
    return os.path.exists(DISTRIBUTIONS_PATH)

# Check if data exists; if not, show warning and helper button
if not check_data():
    st.warning("Data is processing. Please check the GitHub Actions tab.")
    if st.button("Check for Data"):
        if check_data():
            st.rerun()
        else:
            st.error("Data files are still missing. Please wait for the GitHub Action to finish.")
    st.stop()

# Load data once available
try:
    with open(DISTRIBUTIONS_PATH, "r") as f:
        player_data = json.load(f)
except Exception as e:
    st.error(f"Error loading player distributions: {e}")
    st.stop()

# Main Dashboard Interface
st.subheader("Player Performance Distributions")

if player_data:
    # Display player distributions as a selectable dataframe or interactive metrics
    df_dist = pd.DataFrame.from_dict(player_data, orient='index')
    st.dataframe(df_dist, use_container_width=True)
else:
    st.info("No distribution data available yet.")

# Optional: Audit Results Section
if os.path.exists(AUDIT_PATH):
    st.subheader("Audit & Model Accuracy Loop")
    try:
        with open(AUDIT_PATH, "r") as f:
            audit_data = json.load(f)
            if audit_data:
                st.dataframe(pd.DataFrame(audit_data), use_container_width=True)
            else:
                st.write("Audit results file is currently empty.")
    except Exception as e:
        st.warning(f"Could not load audit results: {e}")

# Footer / Refresh Action
if st.button("Refresh Data"):
    st.rerun()
p
