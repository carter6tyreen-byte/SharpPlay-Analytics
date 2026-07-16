import streamlit as st
import pandas as pd

# 1. Title of your app
st.title("SharpPLAY Analytics Dashboard")

# 2. Logic to load the data
# We use st.cache_data so the app doesn't re-load the file every time you click something
@st.cache_data
def load_data():
    return pd.read_json("analytics_data.json")

data = load_data()

# 3. Logic to display the data
st.write("Here is the latest data from our automated pipeline:")
st.dataframe(data)

# 4. Logic to draw a chart (assuming your JSON has columns like 'Date' and 'Value')
st.subheader("Trends")
st.line_chart(data)
