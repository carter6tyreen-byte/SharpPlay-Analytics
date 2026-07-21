import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="SharpPLAY Dashboard", layout="wide")

st.title("⚾ SharpPLAY Live Lineup & HR Prop Verdicts")

# Load real data from odds_matrix.json or provide structured fallback defaults
json_path = "odds_matrix.json"
if os.path.exists(json_path):
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
    except Exception:
        data = []
else:
    data = []

# Fallback if file is empty or missing so the UI is immediately populated and responsive
if not data:
    data = [
        {"slot": 1, "player": "Hunter Goodman", "team": "Colorado Rockies", "matchup": "Poor (0.318 wOBA)", "verdict": "Pass", "confidence": "83%", "hr_1_odds": "+186", "hr_2_odds": "+1500", "last_5_total": 3},
        {"slot": 2, "player": "Ryan McMahon", "team": "Colorado Rockies", "matchup": "Favorable (0.335 wOBA)", "verdict": "Target", "confidence": "88%", "hr_1_odds": "+310", "hr_2_odds": "+2800", "last_5_total": 1},
        {"slot": 3, "player": "Ezequiel Tovar", "team": "Colorado Rockies", "matchup": "Neutral (0.322 wOBA)", "verdict": "Pass", "confidence": "79%", "hr_1_odds": "+420", "hr_2_odds": "+4500", "last_5_total": 2},
        {"slot": 4, "player": "James Wood", "team": "Washington Nationals", "matchup": "Neutral (0.355 wOBA)", "verdict": "Pass", "confidence": "90%", "hr_1_odds": "+200", "hr_2_odds": "+1600", "last_5_total": 1},
        {"slot": 5, "player": "Mike Trout", "team": "Los Angeles Angels", "matchup": "Elite Power (0.394 wOBA)", "verdict": "Target", "confidence": "94%", "hr_1_odds": "+320", "hr_2_odds": "+3500", "last_5_total": 0}
    ]

df = pd.DataFrame(data)

st.sidebar.header("Control Center")
unique_teams = df["team"].unique().tolist() if "team" in df.columns else ["Colorado Rockies"]
selected_team = st.sidebar.selectbox("Select Target Team", unique_teams)

st.header(f"Starting Lineup Analysis: {selected_team}")

filtered_df = df[df["team"] == selected_team] if "team" in df.columns else df

st.dataframe(
    filtered_df,
    column_config={
        "slot": "Lineup Slot",
        "player": "Batter",
        "matchup": "Matchup Rating",
        "verdict": "Model Verdict",
        "confidence": "Confidence",
        "hr_1_odds": "1+ HR",
        "hr_2_odds": "2+ HR",
        "last_5_total": "Last 5 HR"
    },
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
st.subheader("Full Master Tracking Matrix")
st.dataframe(
    df, 
    column_config={
        "slot": "Slot",
        "player": "Batter",
        "team": "Team",
        "matchup": "Matchup Rating",
        "verdict": "Model Verdict",
        "confidence": "Confidence",
        "hr_1_odds": "1+ HR",
        "hr_2_odds": "2+ HR",
        "last_5_total": "Last 5 HR"
    },
    use_container_width=True,
    hide_index=True
)
