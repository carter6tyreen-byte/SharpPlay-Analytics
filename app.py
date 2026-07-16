import streamlit as st
import pandas as pd
import os

st.title("📊 SharpPLAY Analytics Dashboard")

# Improved search logic: look for the file in the current directory and subdirectories
def find_data_file(filename):
    for root, dirs, files in os.walk("."):
        if filename in files:
            return os.path.join(root, filename)
    return None

data_path = find_data_file("analytics_data.json")

if data_path:
    df = pd.read_json(data_path)
    st.write("### Latest Data Summary")
    st.dataframe(df, use_container_width=True)
    st.line_chart(df)
else:
    st.warning("Data file not found. Ensure the pipeline ran successfully and the file exists.")
