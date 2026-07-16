import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="SharpPLAY Analytics", layout="wide")
st.title("📊 SharpPLAY Analytics Dashboard")

# Ensure this URL matches your actual file name exactly
DATA_URL = "https://raw.githubusercontent.com/carter6tyreen-byte/SharpPlay-Analytics/main/today_matchups.json"

@st.cache_data(ttl=600)
def load_data():
    try:
        response = requests.get(DATA_URL).json()
        game_data = response['dates'][0]['games'][0]
        
        data = {
            "Matchup": [f"{game_data['teams']['away']['team']['name']} @ {game_data['teams']['home']['team']['name']}"],
            "Venue": [game_data['venue']['name']],
            "Date": [game_data['gameDate']],
            "Status": [game_data['status']['detailedState']]
        }
        return pd.DataFrame(data)
    except Exception as e:
        return None

df = load_data()

if df is not None:
    st.write("### Today's MLB Matchups")
    st.table(df)
else:
    st.error("Could not load or parse 'today_matchups.json'.")

