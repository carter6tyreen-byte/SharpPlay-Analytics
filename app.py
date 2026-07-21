import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="SharpPLAY Dashboard", layout="wide")

st.title("⚾ SharpPLAY Live Lineup & HR Prop Verdicts")

# Load real data from odds_matrix.json or fallback to defaults
json_path = "odds_matrix.json"
if os.path.exists(json_path):
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except Exception:
        data = []
else:
    data = []

if not data:
    data = [
        {"player": "Hunter Goodman", "team": "Colorado Rockies", "hr_1_odds": "+186", "hr_2_odds": "+1500", "last_5_total": 3},
        {"player": "James Wood", "team": "Washington Nationals", "hr_1_odds": "+200", "hr_2_odds": "+1600", "last_5_total": 1},
        {"player": "Mike Trout", "team": "Los Angeles Angels", "hr_1_odds": "+320", "hr_2_odds": "+3500", "last_5_total": 0}
    ]

df = pd.DataFrame(data)

st.subheader("Active Tracking Matrix & Evaluated Props")

st.dataframe(
    df, 
    column_config={
        "player": "Batter",
        "team": "Team",
        "hr_1_odds": "1+ HR Odds",
        "hr_2_odds": "2+ HR Odds",
        "last_5_total": "Last 5 HR"
    },
    use_container_width=True,
    hide_index=True
)

st.sidebar.header("Filter Options")
unique_teams = df["team"].unique() if "team" in df.columns else ["Colorado Rockies"]
selected_team = st.sidebar.selectbox("Select Team", unique_teams)

filtered_df = df[df["team"] == selected_team] if "team" in df.columns else df
st.subheader(f"Lineup for {selected_team}")

lineup_columns = [col for col in ['player', 'hr_1_odds', 'hr_2_odds', 'last_5_total'] if col in filtered_df.columns]

st.dataframe(
    filtered_df[lineup_columns],
    column_config={
        "player": "Batter",
        "hr_1_odds": "1+ HR Odds",
        "hr_2_odds": "2+ HR Odds",
        "last_5_total": "Last 5 HR"
    },
    use_container_width=True,
    hide_index=True
)
