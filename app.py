import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="SharpPLAY Dashboard", layout="wide")

st.title("⚾ SharpPLAY Full-Slate Lineup & Matchup Matrix")

# Load real multi-game data or fallback to full-slate defaults mirroring professional layout
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
        # Game: PHI @ LAD
        {
            "game": "PHI @ LAD",
            "team": "Philadelphia Phillies",
            "opp_pitcher": "Justin Wrobleski (LHP)",
            "batting_order": 1,
            "player": "T. Turner",
            "bats": "R",
            "ab": 2,
            "h": 0,
            "hr": 0,
            "avg": 0.000,
            "slg": 0.000,
            "k_pct": 0.0,
            "brl_pct": 0.0,
            "prop_type": "HRs",
            "prop_line": 0.5,
            "odds": "+500"
        },
        {
            "game": "PHI @ LAD",
            "team": "Philadelphia Phillies",
            "opp_pitcher": "Justin Wrobleski (LHP)",
            "batting_order": 2,
            "player": "K. Schwarber",
            "bats": "L",
            "ab": 4,
            "h": 2,
            "hr": 1,
            "avg": 0.500,
            "slg": 1.250,
            "k_pct": 25.0,
            "brl_pct": 33.3,
            "prop_type": "HRs",
            "prop_line": 0.5,
            "odds": "+251"
        },
        {
            "game": "PHI @ LAD",
            "team": "Philadelphia Phillies",
            "opp_pitcher": "Justin Wrobleski (LHP)",
            "batting_order": 3,
            "player": "B. Harper",
            "bats": "L",
            "ab": 4,
            "h": 1,
            "hr": 0,
            "avg": 0.250,
            "slg": 0.500,
            "k_pct": 50.0,
            "brl_pct": 0.0,
            "prop_type": "HRs",
            "prop_line": 0.5,
            "odds": "+475"
        },
        {
            "game": "PHI @ LAD",
            "team": "Philadelphia Phillies",
            "opp_pitcher": "Justin Wrobleski (LHP)",
            "batting_order": 4,
            "player": "A. Bohm",
            "bats": "R",
            "ab": 3,
            "h": 0,
            "hr": 0,
            "avg": 0.000,
            "slg": 0.000,
            "k_pct": 0.0,
            "brl_pct": 0.0,
            "prop_type": "HRs",
            "prop_line": 0.5,
            "odds": "+650"
        },
        {
            "game": "PHI @ LAD",
            "team": "Philadelphia Phillies",
            "opp_pitcher": "Justin Wrobleski (LHP)",
            "batting_order": 5,
            "player": "E. Sosa",
            "bats": "R",
            "ab": 0,
            "h": 0,
            "hr": 0,
            "avg": 0.0,
            "slg": 0.0,
            "k_pct": 0.0,
            "brl_pct": 0.0,
            "prop_type": "HRs",
            "prop_line": 0.5,
            "odds": "+750"
        },
        {
            "game": "PHI @ LAD",
            "team": "Philadelphia Phillies",
            "opp_pitcher": "Justin Wrobleski (LHP)",
            "batting_order": 6,
            "player": "B. Marsh",
            "bats": "L",
            "ab": 3,
            "h": 1,
            "hr": 1,
            "avg": 0.333,
            "slg": 1.333,
            "k_pct": 66.7,
            "brl_pct": 100.0,
            "prop_type": "HRs",
            "prop_line": 0.5,
            "odds": "+625"
        },
        {
            "game": "PHI @ LAD",
            "team": "Philadelphia Phillies",
            "opp_pitcher": "Justin Wrobleski (LHP)",
            "batting_order": 7,
            "player": "J. Realmuto",
            "bats": "R",
            "ab": 2,
            "h": 0,
            "hr": 0,
            "avg": 0.000,
            "slg": 0.000,
            "k_pct": 50.0,
            "brl_pct": 0.0,
            "prop_type": "HRs",
            "prop_line": 0.5,
            "odds": "+650"
        },
        {
            "game": "PHI @ LAD",
            "team": "Philadelphia Phillies",
            "opp_pitcher": "Justin Wrobleski (LHP)",
            "batting_order": 8,
            "player": "D. Hill",
            "bats": "R",
            "ab": 0,
            "h": 0,
            "hr": 0,
            "avg": 0.0,
            "slg": 0.0,
            "k_pct": 0.0,
            "brl_pct": 0.0,
            "prop_type": "HRs",
            "prop_line": 0.5,
            "odds": "+650"
        },
        {
            "game": "PHI @ LAD",
            "team": "Philadelphia Phillies",
            "opp_pitcher": "Justin Wrobleski (LHP)",
            "batting_order": 9,
            "player": "B. Stott",
            "bats": "L",
            "ab": 4,
            "h": 0,
            "hr": 0,
            "avg": 0.000,
            "slg": 0.000,
            "k_pct": 25.0,
            "brl_pct": 0.0,
            "prop_type": "HRs",
            "prop_line": 0.5,
            "odds": "+950"
        },
        # Opponent Game: LAD Batting
        {
            "game": "PHI @ LAD",
            "team": "Los Angeles Dodgers",
            "opp_pitcher": "Zack Wheeler (RHP)",
            "batting_order": 1,
            "player": "S. Ohtani",
            "bats": "L",
            "ab": 6,
            "h": 4,
            "hr": 1,
            "avg": 0.667,
            "slg": 1.167,
            "k_pct": 33.3,
            "brl_pct": 25.0,
            "prop_type": "HRs",
            "prop_line": 0.5,
            "odds": "+251"
        },
        {
            "game": "PHI @ LAD",
            "team": "Los Angeles Dodgers",
            "opp_pitcher": "Zack Wheeler (RHP)",
            "batting_order": 2,
            "player": "A. Pages",
            "bats": "R",
            "ab": 3,
            "h": 0,
            "hr": 0,
            "avg": 0.000,
            "slg": 0.000,
            "k_pct": 0.0,
            "brl_pct": 0.0,
            "prop_type": "HRs",
            "prop_line": 0.5,
            "odds": "+600"
        },
        {
            "game": "PHI @ LAD",
            "team": "Los Angeles Dodgers",
            "opp_pitcher": "Zack Wheeler (RHP)",
            "batting_order": 3,
            "player": "F. Freeman",
            "bats": "L",
            "ab": 28,
            "h": 8,
            "hr": 1,
            "avg": 0.286,
            "slg": 0.429,
            "k_pct": 14.3,
            "brl_pct": 0.0,
            "prop_type": "HRs",
            "prop_line": 0.5,
            "odds": "+500"
        },
        {
            "game": "PHI @ LAD",
            "team": "Los Angeles Dodgers",
            "opp_pitcher": "Zack Wheeler (RHP)",
            "batting_order": 4,
            "player": "M. Betts",
            "bats": "R",
            "ab": 8,
            "h": 0,
            "hr": 0,
            "avg": 0.000,
            "slg": 0.000,
            "k_pct": 25.0,
            "brl_pct": 0.0,
            "prop_type": "HRs",
            "prop_line": 0.5,
            "odds": "+700"
        },
        {
            "game": "PHI @ LAD",
            "team": "Los Angeles Dodgers",
            "opp_pitcher": "Zack Wheeler (RHP)",
            "batting_order": 5,
            "player": "M. Muncy",
            "bats": "L",
            "ab": 4,
            "h": 1,
            "hr": 1,
            "avg": 0.250,
            "slg": 1.000,
            "k_pct": 50.0,
            "brl_pct": 0.0,
            "prop_type": "HRs",
            "prop_line": 0.5,
            "odds": "+430"
        },
        {
            "game": "PHI @ LAD",
            "team": "Los Angeles Dodgers",
            "opp_pitcher": "Zack Wheeler (RHP)",
            "batting_order": 6,
            "player": "K. Tucker",
            "bats": "L",
            "ab": 11,
            "h": 1,
            "hr": 1,
            "avg": 0.091,
            "slg": 0.364,
            "k_pct": 27.3,
            "brl_pct": 12.5,
            "prop_type": "HRs",
            "prop_line": 0.5,
            "odds": "+650"
        },
        {
            "game": "PHI @ LAD",
            "team": "Los Angeles Dodgers",
            "opp_pitcher": "Zack Wheeler (RHP)",
            "batting_order": 7,
            "player": "T. Hernández",
            "bats": "R",
            "ab": 5,
            "h": 1,
            "hr": 1,
            "avg": 0.200,
            "slg": 0.800,
            "k_pct": 40.0,
            "brl%": 33.3,
            "prop_type": "HRs",
            "prop_line": 0.5,
            "odds": "+700"
        },
        {
            "game": "PHI @ LAD",
            "team": "Los Angeles Dodgers",
            "opp_pitcher": "Zack Wheeler (RHP)",
            "batting_order": 8,
            "player": "D. Rushing",
            "bats": "L",
            "ab": 0,
            "h": 0,
            "hr": 0,
            "avg": 0.0,
            "slg": 0.0,
            "k_pct": 0.0,
            "brl_pct": 0.0,
            "prop_type": "HRs",
            "prop_line": 0.5,
            "odds": "+500"
        },
        {
            "game": "PHI @ LAD",
            "team": "Los Angeles Dodgers",
            "opp_pitcher": "Zack Wheeler (RHP)",
            "batting_order": 9,
            "player": "T. Edman",
            "bats": "SW",
            "ab": 14,
            "h": 3,
            "hr": 0,
            "avg": 0.214,
            "slg": 0.214,
            "k_pct": 35.7,
            "brl_pct": 0.0,
            "prop_type": "HRs",
            "prop_line": 0.5,
            "odds": "+1000"
        }
    ]

df = pd.DataFrame(data)

# Sidebar Controls for Full-Slate Game and Prop Dissection
st.sidebar.header("Control Center")
unique_games = df["game"].unique().tolist() if "game" in df.columns else []
selected_game = st.sidebar.selectbox("Select Game Slate", unique_games)

game_df = df[df["game"] == selected_game] if "game" in df.columns else df

unique_teams = game_df["team"].unique().tolist() if "team" in game_df.columns else []
selected_team = st.sidebar.selectbox("Select Batting Order / Lineup", unique_teams)

filtered_df = game_df[game_df["team"] == selected_team] if "game" in game_df.columns else game_df

# Interactive Prop Market Switcher in Sidebar (HRs, Hits, Ks, etc.)
prop_options = ["HRs", "Hits", "RBIs", "Bases", "Runs"]
selected_prop = st.sidebar.selectbox("Select Stat / Prop Market", prop_options)

if not filtered_df.empty:
    opp_sp = filtered_df.iloc[0]["opp_pitcher"]
    lh_count = len(filtered_df[filtered_df["bats"] == "L"])
    rh_count = len(filtered_df[filtered_df["bats"] == "R"])
    sw_count = len(filtered_df[filtered_df["bats"] == "SW"])
    st.markdown(f"### {selected_team} Batting Order")
    st.caption(f"Expected Lineup vs. {opp_sp} | {lh_count} LHB, {rh_count} RHB, {sw_count} SW")

# Format columns cleanly for professional matchup display
display_df = filtered_df[["batting_order", "player", "bats", "ab", "h", "hr", "avg", "slg", "k_pct", "brl_pct", "prop_line", "odds"]].copy()

display_df.columns = [
    "Order", "Batter", "Bats", "AB", "H", "HR", "AVG", "SLG", "K%", "BRL%", "Line", "Odds"
]

st.dataframe(
    display_df,
    column_config={
        "Order": st.column_config.NumberColumn("Order", format="%d"),
        "Batter": "Batter",
        "Bats": "Bats",
        "AB": st.column_config.NumberColumn("AB", format="%d"),
        "H": st.column_config.NumberColumn("H", format="%d"),
        "HR": st.column_config.NumberColumn("HR", format="%d"),
        "AVG": st.column_config.NumberColumn("AVG", format="%.3f"),
        "SLG": st.column_config.NumberColumn("SLG", format="%.3f"),
        "K%": st.column_config.NumberColumn("K%", format="%.1f%%"),
        "BRL%": st.column_config.NumberColumn("BRL%", format="%.1f%%"),
        "Line": st.column_config.NumberColumn("Line", format="%.1f"),
        "Odds": "Odds"
    },
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
st.subheader("Full Master Slate Matrix")
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)
