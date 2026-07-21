import streamlit as st
import pandas as pd
import json
import os
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="SharpPLAY Dashboard", layout="wide")

st.title("⚾ SharpPLAY Full-Slate Matchup & Arsenal Matrix")

def filter_confirmed_lineups(optimizer_df, rotowire_lineups_df):
    player_col = 'player' if 'player' in optimizer_df.columns else 'Player'
    rot_player_col = 'player' if 'player' in rotowire_lineups_df.columns else 'Player'
    
    optimizer_df['clean_name'] = optimizer_df[player_col].astype(str).str.strip().str.lower()
    rotowire_lineups_df['clean_name'] = rotowire_lineups_df[rot_player_col].astype(str).str.strip().str.lower()
    
    confirmed_players = set(rotowire_lineups_df[rotowire_lineups_df['is_confirmed'] == True]['clean_name'])
    
    filtered_df = optimizer_df[optimizer_df['clean_name'].isin(confirmed_players)].copy()
    filtered_df['locked'] = True
    
    return filtered_df

@st.cache_data(ttl=600)
def fetch_live_rotowire_lineups():
    confirmed_dict = {}
    url = "https://www.rotowire.com/baseball/mlb-lineups.php"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            players = soup.find_all('li', class_='lineup__player')
            for p in players:
                p_name = p.get_text(strip=True)
                clean_name = ''.join([c for c in p_name if c.isalpha() or c == ' ']).strip().lower()
                confirmed_dict[clean_name] = True
    except Exception:
        pass
        
    return confirmed_dict

fallback_data = [
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
        "odds": "+500",
        "is_confirmed": True
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
        "odds": "+251",
        "is_confirmed": True
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
        "odds": "+475",
        "is_confirmed": True
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
        "odds": "+650",
        "is_confirmed": True
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
        "odds": "+750",
        "is_confirmed": False
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
        "odds": "+625",
        "is_confirmed": True
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
        "odds": "+650",
        "is_confirmed": True
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
        "odds": "+650",
        "is_confirmed": False
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
        "odds": "+950",
        "is_confirmed": True
    },
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
        "odds": "+251",
        "is_confirmed": True
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
        "odds": "+600",
        "is_confirmed": True
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
        "odds": "+500",
        "is_confirmed": True
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
        "odds": "+700",
        "is_confirmed": True
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
        "odds": "+430",
        "is_confirmed": True
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
        "odds": "+650",
        "is_confirmed": True
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
        "brl_pct": 33.3,
        "prop_type": "HRs",
        "prop_line": 0.5,
        "odds": "+700",
        "is_confirmed": True
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
        "odds": "+500",
        "is_confirmed": False
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
        "odds": "+1000",
        "is_confirmed": True
    }
]

json_path = "odds_matrix.json"
data = []
if os.path.exists(json_path):
    try:
        with open(json_path, "r") as f:
            content = f.read().strip()
            if content:
                data = json.loads(content)
    except Exception:
        data = []

if not data:
    data = fallback_data

df_raw = pd.DataFrame(data)

p_col = 'player' if 'player' in df_raw.columns else ('Player' if 'Player' in df_raw.columns else None)
if not p_col:
    df_raw['player'] = "Unknown"
    p_col = 'player'

if 'is_confirmed' not in df_raw.columns:
    df_raw['is_confirmed'] = True

live_confirmed = fetch_live_rotowire_lineups()

rotowire_ref_df = df_raw[[p_col, 'is_confirmed']].copy()
rotowire_ref_df.rename(columns={p_col: 'player'}, inplace=True)

if live_confirmed:
    rotowire_ref_df['is_confirmed'] = rotowire_ref_df['player'].apply(
        lambda x: ''.join([c for c in str(x) if c.isalpha() or c == ' ']).strip().lower() in live_confirmed
    )

if p_col != 'player':
    df_raw.rename(columns={p_col: 'player'}, inplace=True)

df = filter_confirmed_lineups(df_raw, rotowire_ref_df)

st.sidebar.header("Control Center")
require_confirmation = st.sidebar.checkbox("Lock Confirmed Lineups Only", value=True)

if require_confirmation and "is_confirmed" in df.columns:
    df = df[df["is_confirmed"] == True].copy()

unique_games = df["game"].unique().tolist() if "game" in df.columns and not df.empty else []

if not unique_games:
    st.error("No confirmed lineup data available.")
    st.stop()

selected_game = st.sidebar.selectbox("Select Game Slate", unique_games)
game_df = df[df["game"] == selected_game] if "game" in df.columns else df

teams = game_df["team"].unique().tolist() if "team" in game_df.columns else []

st.markdown(f"## ⚔️ Game Matchup View: {selected_game}")

col1, col2 = st.columns(2)

selected_batter = None

def render_team_column(team_name, container):
    global selected_batter
    with container:
        team_df = game_df[game_df["team"] == team_name]
        opp_sp = team_df.iloc[0].get("opp_pitcher", "TBD") if not team_df.empty else "TBD"
        st.subheader(f"{team_name}")
        st.caption(f"Facing Opposing Pitcher: {opp_sp}")
        
        if not team_df.empty:
            display_cols = ["batting_order", "player", "bats", "ab", "h", "hr", "avg", "slg", "odds"]
            available_cols = [c for c in display_cols if c in team_df.columns]
            st.dataframe(team_df[available_cols], use_container_width=True, hide_index=True)
            
            player_list = team_df["player"].tolist()
            chosen = st.selectbox(f"Select Batter ({team_name})", player_list, key=f"sel_{team_name}")
            if chosen:
                selected_batter = chosen

if len(teams) >= 2:
    with col1:
        render_team_column(teams[0], col1)
    with col2:
        render_team_column(teams[1], col2)
elif len(teams) == 1:
    render_team_column(teams[0], col1)

st.markdown("---")
st.markdown("### 🔬 StarWorld Pitcher Arsenal & Batter Deep-Dive")

if selected_batter:
    batter_row = game_df[game_df["player"] == selected_batter]
    if not batter_row.empty:
        b_data = batter_row.iloc[0]
        st.success(f"Loaded Deep-Dive for **{selected_batter}** ({b_data.get('team', '')}) vs {b_data.get('opp_pitcher', '')}")
        
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            st.metric("Batting Average vs Pitcher Type", f"{b_data.get('avg', 0.0):.3f}")
            st.metric("At-Bats Sample Size", int(b_data.get('ab', 0)))
        with col_b:
            st.metric("Slugging Percentage", f"{b_data.get('slg', 0.0):.3f}")
            st.metric("Home Run Prop Odds", b_data.get('odds', 'N/A'))
        with col_c:
            st.metric("Strikeout Rate (K%)", f"{b_data.get('k_pct', 0.0)}%")
            st.metric("Barrel Rate", f"{b_data.get('brl_pct', 0.0)}%")
        
        st.info("💡 **StarWorld Arsenal Insight:** Tracking pitch-mix tracking metrics, velocity splits, and optimal launch angle zones against opposing starter's primary pitch catalog.")
else:
    st.info("Select a batter from either team's lineup above to load the StarWorld pitch-arsenal breakdown.")
