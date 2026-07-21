import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="SharpPLAY Dashboard", layout="wide")

st.title("⚾ SharpPLAY Live Lineup & HR Prop Verdicts")

# Load odds matrix data safely
try:
    with open("odds_matrix.json", "r") as f:
        data = json.load(f)
except Exception:
    data = [
        {"player": "Hunter Goodman", "team": "Colorado Rockies", "hr_1_odds": "+186", "hr_2_odds": "+1500", "last_5_total": 3},
        {"player": "James Wood", "team": "Washington Nationals", "hr_1_odds": "+200", "hr_2_odds": "+1600", "last_5_total": 1},
        {"player": "Mike Trout", "team": "Los Angeles Angels", "hr_1_odds": "+320", "hr_2_odds": "+3500", "last_5_total": 0}
    ]

df = pd.DataFrame(data)

st.subheader("Active Tracking Matrix & Evaluated Props")

# Use container width configuration compatible with current Streamlit builds
st.dataframe(df, use_container_width=True)

st.sidebar.header("Filter Options")
unique_teams = df["team"].unique() if "team" in df.columns else ["Colorado Rockies"]
selected_team = st.sidebar.selectbox("Select Team", unique_teams)

filtered_df = df[df["team"] == selected_team] if "team" in df.columns else df
st.subheader(f"Lineup for {selected_team}")

display_columns = [col for col in ['player', 'hr_1_odds', 'hr_2_odds', 'last_5_total'] if col in filtered_df.columns]
st.table(filtered_df[display_columns])
