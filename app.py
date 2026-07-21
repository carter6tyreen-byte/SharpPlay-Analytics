import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="SharpPLAY Dashboard", layout="wide")

st.title("⚾ SharpPLAY Full-Slate Pitch-Mix & Lineup Dissector")

# Load real multi-game data or initialize full slate structure across multiple games & pitchers
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
        # Game 1: Rockies @ Dodgers
        {
            "game": "COL @ LAD",
            "team": "Colorado Rockies",
            "opp_pitcher": "Tyler Glasnow (RHP)",
            "pitcher_primary_mix": "4-Seam (52%) / Slider (28%)",
            "batting_order": 1,
            "player": "Hunter Goodman",
            "woba_vs_mix": "0.318",
            "iso_vs_mix": "0.195",
            "hr_1_odds": "+186",
            "hr_2_odds": "+1500",
            "verdict": "Pass"
        },
        {
            "game": "COL @ LAD",
            "team": "Colorado Rockies",
            "opp_pitcher": "Tyler Glasnow (RHP)",
            "pitcher_primary_mix": "4-Seam (52%) / Slider (28%)",
            "batting_order": 2,
            "player": "Ryan McMahon",
            "woba_vs_mix": "0.335",
            "iso_vs_mix": "0.220",
            "hr_1_odds": "+310",
            "hr_2_odds": "+2800",
            "verdict": "Target"
        },
        {
            "game": "COL @ LAD",
            "team": "Colorado Rockies",
            "opp_pitcher": "Tyler Glasnow (RHP)",
            "pitcher_primary_mix": "4-Seam (52%) / Slider (28%)",
            "batting_order": 3,
            "player": "Ezequiel Tovar",
            "woba_vs_mix": "0.322",
            "iso_vs_mix": "0.175",
            "hr_1_odds": "+420",
            "hr_2_odds": "+4500",
            "verdict": "Pass"
        },
        # Game 2: Yankees @ Red Sox
        {
            "game": "NYY @ BOS",
            "team": "New York Yankees",
            "opp_pitcher": "Brayan Bello (RHP)",
            "pitcher_primary_mix": "Sinker (46%) / Changeup (30%)",
            "batting_order": 1,
            "player": "Anthony Volpe",
            "woba_vs_mix": "0.325",
            "iso_vs_mix": "0.165",
            "hr_1_odds": "+450",
            "hr_2_odds": "+4000",
            "verdict": "Pass"
        },
        {
            "game": "NYY @ BOS",
            "team": "New York Yankees",
            "opp_pitcher": "Brayan Bello (RHP)",
            "pitcher_primary_mix": "Sinker (46%) / Changeup (30%)",
            "batting_order": 2,
            "player": "Juan Soto",
            "woba_vs_mix": "0.442",
            "iso_vs_mix": "0.310",
            "hr_1_odds": "+220",
            "hr_2_odds": "+1800",
            "verdict": "Target"
        },
        {
            "game": "NYY @ BOS",
            "team": "New York Yankees",
            "opp_pitcher": "Brayan Bello (RHP)",
            "pitcher_primary_mix": "Sinker (46%) / Changeup (30%)",
            "batting_order": 3,
            "player": "Aaron Judge",
            "woba_vs_mix": "0.485",
            "iso_vs_mix": "0.390",
            "hr_1_odds": "+175",
            "hr_2_odds": "+1100",
            "verdict": "Target"
        }
    ]

df = pd.DataFrame(data)

st.sidebar.header("Full Slate Controls")
unique_games = df["game"].unique().tolist() if "game" in df.columns else []
selected_game = st.sidebar.selectbox("Select Matchup / Game", unique_games)

game_df = df[df["game"] == selected_game] if "game" in df.columns else df

unique_teams = game_df["team"].unique().tolist() if "team" in game_df.columns else []
selected_team = st.sidebar.selectbox("Select Team Lineup", unique_teams)

filtered_df = game_df[game_df["team"] == selected_team] if "team" in game_df.columns else game_df

# Display context banner for the selected matchup and pitcher mix
if not filtered_df.empty:
    opp_sp = filtered_df.iloc[0]["opp_pitcher"]
    mix_profile = filtered_df.iloc[0]["pitcher_primary_mix"]
    st.info(f"**Matchup Breakdown:** {selected_team} vs. **{opp_sp}** | **Opponent Pitch Mix Profile:** {mix_profile}")

st.header(f"Starting 9 vs. Pitch Mix Analysis: {selected_team}")

column_configuration = {
    "batting_order": st.column_config.NumberColumn("Order", format="%d"),
    "player": "Batter",
    "woba_vs_mix": "wOBA vs Mix",
    "iso_vs_mix": "ISO vs Mix",
    "hr_1_odds": "1+ HR Odds",
    "hr_2_odds": "2+ HR Odds",
    "verdict": "Model Verdict"
}

st.dataframe(
    filtered_df[["batting_order", "player", "woba_vs_mix", "iso_vs_mix", "hr_1_odds", "hr_2_odds", "verdict"]],
    column_config=column_configuration,
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
st.subheader("Complete Game Slate Master Matrix (All Games & Lineups)")
st.dataframe(
    df, 
    column_config={
        "game": "Game",
        "team": "Team",
        "opp_pitcher": "Opposing Pitcher",
        "pitcher_primary_mix": "Pitch Mix Profile",
        "batting_order": "Order",
        "player": "Batter",
        "woba_vs_mix": "wOBA vs Mix",
        "iso_vs_mix": "ISO vs Mix",
        "hr_1_odds": "1+ HR",
        "hr_2_odds": "2+ HR",
        "verdict": "Verdict"
    },
    use_container_width=True,
    hide_index=True
)
