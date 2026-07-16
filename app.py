import streamlit as st
import pandas as pd

st.set_page_config(page_title="SharpPLAY Analytics", layout="wide")
st.title("📊 SharpPLAY Analytics Dashboard")

# Load data directly from your GitHub repository's raw URL
# Replace 'carter6tyreen-byte' and 'SharpPlay-Analytics' with your actual username/repo
DATA_URL = "https://raw.githubusercontent.com/carter6tyreen-byte/SharpPlay-Analytics/main/analytics_data.json"

@st.cache_data(ttl=60) # Automatically refresh the data every 60 seconds
def load_data():
    try:
        return pd.read_json(DATA_URL)
    except Exception as e:
        return None

df = load_data()

if df is not None:
    st.write("### Latest Data Summary")
    st.dataframe(df, use_container_width=True)
    st.line_chart(df)
else:
    st.error("Could not load data. Ensure the pipeline has pushed 'analytics_data.json' to the main branch.")
