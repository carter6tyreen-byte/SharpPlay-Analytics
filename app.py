import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="SharpPLAY Analytics", layout="wide")
st.title("📊 SharpPLAY Analytics Dashboard")

# The exact path to your file
DATA_URL = "https://raw.githubusercontent.com/carter6tyreen-byte/SharpPlay-Analytics/main/today_matchups.json"

@st.cache_data(ttl=600)
def load_data():
    try:
        response = requests.get(DATA_URL).json()
        # Navigate the JSON structure: dates -> games
        game_data = response['dates'][0]['games'][0]
        
        # Flatten the data for a nice table
        data = {
            "Game": [f"{game_data['teams']['away']['team']['name']} @ {game_data['teams']['home']['team']['name']}"],
            "Venue": [game_data['venue']['name']],
            "Time (UTC)": [game_data['gameDate']],
            "Status": [game_data['status']['detailedState']]
        }
        return pd.DataFrame(data)
    except Exception as e:
        return None

df = load_data()

if df is not None:
    st.write("### Today's Matchup")
    st.table(df)
else:
    st.error("Could not parse 'today_matchups.json'. Check if the file is available.")
