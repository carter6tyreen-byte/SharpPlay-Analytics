import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="SharpPLAY Analytics", layout="wide")
st.title("📊 SharpPLAY Analytics Dashboard")

# 1. Use the exact RAW URL for your file
DATA_URL = "https://raw.githubusercontent.com/carter6tyreen-byte/SharpPlay-Analytics/main/today_matchups.json"

# 2. Use a short cache TTL (Time-To-Live) to ensure it fetches fresh data
@st.cache_data(ttl=60) 
def load_data():
    try:
        response = requests.get(DATA_URL)
        if response.status_code == 200:
            data = response.json()
            # Navigate to the games list
            game = data['dates'][0]['games'][0]
            
            # Format the data for a clean display
            return pd.DataFrame([{
                "Matchup": f"{game['teams']['away']['team']['name']} vs {game['teams']['home']['team']['name']}",
                "Venue": game['venue']['name'],
                "Start Time": game['gameDate'],
                "Status": game['status']['detailedState']
            }])
    except Exception as e:
        return None
    return None

df = load_data()

# 3. Display the data
if df is not None:
    st.write("### Today's Matchup")
    st.table(df)
else:
    st.error("Data not found. Ensure your GitHub Action has successfully pushed 'today_matchups.json' to the main branch.")
