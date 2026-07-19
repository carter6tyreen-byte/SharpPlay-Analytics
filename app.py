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
    st.subheader("Player Performance Distributions")
    
    df_dist = pd.DataFrame.from_dict(player_data, orient='index')
    
    if "status" in df_dist.columns:
        active_only = st.checkbox("Hide Injured Players", value=True)
        if active_only:
            df_dist = df_dist[df_dist["status"].str.lower() != "injured"]
    else:
        hide_injured = st.checkbox("Hide Known Injured Players (Manual Filter)", value=False)
        if hide_injured:
            # Only put genuinely injured/out players here
            injured_list = [] 
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
