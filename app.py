import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="SharpPLAY Analytics", layout="wide")

st.title("📊 SharpPLAY Analytics Dashboard")

# Define the file path
data_file = "analytics_data.json"

# Check if data exists, then load it
if os.path.exists(data_file):
    df = pd.read_json(data_file)
    
    st.write("### Latest Data Summary")
    st.dataframe(df, use_container_width=True)
    
    st.write("### Visual Trends")
    st.line_chart(df)
else:
    st.warning(f"Waiting for data... '{data_file}' not found yet.")
