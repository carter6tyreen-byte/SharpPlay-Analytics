import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Configuration
DATA_URL = "https://raw.githubusercontent.com/carter6tyreen-byte/SharpPlay-Analytics/main/today_matchups.json"

st.set_page_config(page_title="SharpPLAY Analytics", layout="wide")

@st.cache_data(ttl=3600)  # Caches data for 1 hour to reduce network load
def load_data():
    try:
        response = requests.get(DATA_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Use json_normalize to flatten any nested objects (e.g., team stats)
        df = pd.json_normalize(data)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

st.title("⚾ SharpPLAY Analytics Dashboard")

# Refresh mechanism
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

df = load_data()

if df is not None and not df.empty:
    st.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Display the dataframe with interactive features
    st.dataframe(
        df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            # You can add custom formatting here if column names are known
        }
    )
else:
    st.warning("No matchup data available at the moment.")
