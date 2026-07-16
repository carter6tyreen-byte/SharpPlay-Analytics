import streamlit as st
import json
import pandas as pd

# Set page configuration for a professional look
st.set_page_config(page_title="SharpPLAY Dashboard", layout="wide")

st.title("⚾ SharpPLAY Analytics: STARWORLD Engine")

def load_data():
    try:
        # File is now correctly referenced in the root directory
        with open('analytics_data.json', 'r') as f:
            data = json.load(f)
            return pd.DataFrame(data)
    except FileNotFoundError:
        st.error("No data found. Please run the pipeline!")
        return pd.DataFrame()

# Load the data
df = load_data()

# Display the dashboard content
if not df.empty:
    st.subheader("Current Betting Edges")
    st.dataframe(df, use_container_width=True)
    
    st.subheader("Performance Overview")
    # This assumes your data has 'game' and 'edge' columns
    st.bar_chart(df.set_index('game')['edge'])
else:
    st.info("Waiting for data to populate...")
