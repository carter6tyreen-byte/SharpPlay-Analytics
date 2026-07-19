import streamlit as st
import json
import pandas as pd
import requests

st.set_page_config(page_title="SharpPlay Analytics: ODE Optimizer", layout="wide")

st.title("SharpPlay Analytics: ODE Optimizer")

# Direct URL to the raw JSON file on your GitHub repository main branch
# (Make sure to replace USERNAME and REPO with your actual GitHub details if needed)
GITHUB_RAW_URL = "https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME/main/data/player_distributions.json"

@st.cache_data(ttl=60)
def load_data_from_github(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        return None
    return None

# Load the data
player_data = load_data_from_github(GITHUB_RAW_URL)

if player_data:
    st.success("Data successfully loaded from GitHub repository!")
    st.subheader("Player Performance Distributions")
    df_dist = pd.DataFrame.from_dict(player_data, orient='index')
    st.dataframe(df_dist, use_container_width=True)
else:
    st.warning("⚠️ Could not fetch data from GitHub raw URL yet.")
    st.info("Check if your GitHub Action has successfully completed and pushed `data/player_distributions.json` to the `main` branch.")

if st.button("Force Refresh"):
    st.cache_data.clear()
    st.rerun()
