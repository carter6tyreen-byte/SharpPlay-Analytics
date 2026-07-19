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
    
    # 1. Convert JSON to Dataframe
    df_dist = pd.DataFrame.from_dict(player_data, orient='index')
    
    # 2. WHERE IT GOES: Filter Logic 
    # Option A: If your JSON file starts including a "status" key (e.g., "status": "Injured")
    if "status" in df_dist.columns:
        active_only = st.checkbox("Hide Injured Players", value=True)
        if active_only:
            df_dist = df_dist[df_dist["status"].str.lower() != "injured"]
            
    # Option B: Hardcoded fallback UI filter based on Player Names (index) until your data source is updated
    else:
        hide_injured = st.checkbox("Hide Known Injured Players (Manual Filter)", value=False)
        if hide_injured:
            # Add names here to temporarily drop them from the view manually
            injured_list = ["Mookie Betts", "Ronald Acuña Jr."] 
            df_dist = df_dist.drop(index=[name for name in injured_list if name in df_dist.index])

    # 3. Display final filtered dataframe
    st.dataframe(df_dist, use_container_width=True)
else:
    st.error("player_distributions.json not found or could not be parsed in the data directory.")
    
    with st.expander("Container Path Diagnostics"):
        st.write(f"Current Working Directory: {os.getcwd()}")
        if os.path.exists("data"):
            st.write(f"Contents of 'data/' folder: {os.listdir('data')}")

if st.button("Force Refresh"):
    st.rerun()
