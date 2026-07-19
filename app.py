import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="SharpPlay Analytics: ODE Optimizer", layout="wide")

st.title("SharpPlay Analytics: ODE Optimizer")

# Let's check both local direct path and absolute path to be robust against CWD differences
possible_paths = [
    "data/player_distributions.json",
    "./data/player_distributions.json",
    "player_distributions.json"
]

player_data = None
loaded_path = None

for path in possible_paths:
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                content = f.read().strip()
                if content:
                    player_data = json.loads(content)
                    loaded_path = path
                    break
        except Exception as e:
            continue

if player_data:
    st.success(f"Player distributions successfully loaded from `{loaded_path}`!")
    st.subheader("Player Performance Distributions")
    df_dist = pd.DataFrame.from_dict(player_data, orient='index')
    st.dataframe(df_dist, use_container_width=True)
else:
    st.error("player_distributions.json not found in the data directory.")
    
    # Debugging helper to show where we actually are looking
    with st.expander("Container Path Diagnostics"):
        st.write(f"Current Working Directory: {os.getcwd()}")
        if os.path.exists("data"):
            st.write(f"Contents of 'data/' folder: {os.listdir('data')}")
        else:
            st.write("'data' folder not found in current directory.")

if st.button("Force Refresh"):
    st.rerun()
