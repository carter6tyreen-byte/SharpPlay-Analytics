import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="SharpPLAY Dashboard", layout="wide")

st.title("⚾ SharpPLAY Live Lineup & HR Prop Verdicts")

# Load structured odds matrix data
try:
    with open("odds_matrix.json", "r") as f:
        data = json.load(f)
except Exception:
    data = [
        {"player": "Hunter Goodman", "team": "Colorado Rockies", "matchup": "Poor (0.318 wOBA)", "verdict": "Pass", "confidence": "83%", "hr_1_odds": "+186", "hr_2_odds": "+1500", "last_5_total": 3},
        {"player": "James Wood", "team": "Washington Nationals", "matchup": "Neutral (0.355 wOBA)", "verdict": "Pass", "confidence": "90%", "hr_1_odds": "+200", "hr_2_odds": "+1600", "last_5_total": 1},
        {"player": "Mike Trout", "team": "Los Angeles Angels", "matchup": "Elite Power (0.394 wOBA)", "verdict": "Target", "confidence": "94%", "hr_1_odds": "+320", "hr_2_odds": "+3500", "last_5_total": 0}
    ]

df = pd.DataFrame(data)

st.subheader("Active Tracking Matrix & Evaluated Props")

st.dataframe(
    df, 
    column_config={
        "player": "Batter",
        "team": "Team",
        "matchup": "Matchup",
        "verdict": "HR Prop Verdict",
        "confidence": "Confidence",
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

lineup_columns = [col for col in ['player', 'matchup', 'verdict', 'confidence', 'hr_1_odds', 'hr_2_odds', 'last_5_total'] if col in filtered_df.columns]

st.dataframe(
    filtered_df[lineup_columns],
    column_config={
        "player": "Batter",
        "matchup": "Matchup",
        "verdict": "HR Prop Verdict",
        "confidence": "Confidence",
        "hr_1_odds": "1+ HR Odds",
        "hr_2_odds": "2+ HR Odds",
        "last_5_total": "Last 5 HR"
    },
    use_container_width=True,
    hide_index=True
)
