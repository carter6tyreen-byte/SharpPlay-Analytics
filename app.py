import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="SharpPLAY Analytics", layout="wide")
st.title("📊 SharpPLAY Analytics Dashboard")

DATA_URL = "https://raw.githubusercontent.com/carter6tyreen-byte/SharpPlay-Analytics/main/data/today_matchups.json"

@st.cache_data(ttl=60)
def load_data():
    try:
        response = requests.get(DATA_URL)
        if response.status_code == 200:
            data = response.json()
            game = data['dates'][0]['games'][0]
            return pd.DataFrame([{
                "Matchup": f"{game['teams']['away']['team']['name']} vs {game['teams']['home']['team']['name']}",
                "Venue": game['venue']['name'],
                "Start Time": game['gameDate'],
                "Status": game['status']['detailedState']
            }])
    except Exception:
        return None
    return None

# CRITICAL FIX: You must assign the result of load_data() to the variable 'df'
df = load_data()

# Display logic
if df is not None:
    st.write("### ⚾ Today's SharpPLAY Matchups")
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.error("Data could not be loaded.")

# Add a section for potential "Sharp" insights
st.divider()
st.subheader("💡 Today's Insights")
st.info("No game analysis available yet—check back closer to first pitch!")
