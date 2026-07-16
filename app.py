import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="SharpPLAY Analytics", layout="wide")
st.title("📊 SharpPLAY Analytics Dashboard")

# Updated URL with the correct '/data/' path
DATA_URL = "https://raw.githubusercontent.com/carter6tyreen-byte/SharpPlay-Analytics/main/data/today_matchups.json"

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
        else:
            st.error(f"Failed to fetch data. HTTP Status: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error parsing JSON: {e}")
        return None

df = load_data()

# Display the data
if df is not None:
    st.write("### Today's Matchup")
    st.table(df)
