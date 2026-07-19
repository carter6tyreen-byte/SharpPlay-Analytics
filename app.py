import subprocess
import os

# Automatically run the data collector script on app startup to ensure the full slate is loaded
collector_path = os.path.join(os.path.dirname(__file__), "data", "data_collector.py")
if os.path.exists(collector_path):
    try:
        subprocess.run(["python", collector_path], check=True)
    except Exception as e:
        print(f"Error running data collector on startup: {e}")

import subprocess
import os

# Automatically run the data collector script on app startup to ensure the full slate is loaded
collector_path = os.path.join(os.path.dirname(__file__), "data", "data_collector.py")
if os.path.exists(collector_path):
    try:
        subprocess.run(["python", collector_path], check=True)
    except Exception as e:
        print(f"Error running data collector on startup: {e}")
import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="SharpPlay Analytics: ODE Optimizer", layout="wide")

st.title("SharpPlay Analytics: ODE Optimizer")

target_filename = "player_distributions.json"
player_data = None
loaded_path = None

if os.path.exists("data"):
    for filename in os.listdir("data"):
        cleaned_name = filename.encode("ascii", "ignore").decode("utf-8").strip()
        if cleaned_name == target_filename:
            full_path = os.path.join("data", filename)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        player_data = json.loads(content)
                        loaded_path = full_path
                        break
            except Exception as e:
                st.error(f"Error reading {filename}: {e}")

if player_data:
    st.success(f"Player distributions successfully loaded from `{loaded_path}`!")
    st.subheader(f"Player Performance Distributions ({len(player_data)} Players Loaded)")
    
    df_dist = pd.DataFrame.from_dict(player_data, orient='index')
    
    hide_injured = st.checkbox("Hide Known Injured Players (Manual Filter)", value=False)
    if hide_injured:
        injured_list = []  # Keep empty unless specific players are out
        df_dist = df_dist.drop(index=[name for name in injured_list if name in df_dist.index])

    st.dataframe(df_dist, width='stretch')
else:
    st.error("player_distributions.json not found or could not be parsed in the data directory.")
    
    with st.expander("Container Path Diagnostics"):
        st.write(f"Current Working Directory: {os.getcwd()}")
        if os.path.exists("data"):
            st.write(f"Contents of 'data/' folder: {os.listdir('data')}")

if st.button("Force Refresh"):
    st.rerun()
