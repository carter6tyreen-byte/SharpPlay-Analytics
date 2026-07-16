import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="SharpPLAY Dashboard", layout="wide")

st.title("⚾ SharpPLAY Analytics: STARWORLD Engine")

def load_data():
    try:
        with open('data/analytics_data.json', 'r') as f:
            data = json.load(f)
            return pd.DataFrame(data)
    except FileNotFoundError:
        st.error("No data found. Please run the pipeline!")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    st.subheader("Current Betting Edges")
    st.dataframe(df, use_container_width=True)
    
    st.subheader("Performance Overview")
    st.bar_chart(df.set_index('game')['edge'])
else:
    st.info("Waiting for data to populate...")
