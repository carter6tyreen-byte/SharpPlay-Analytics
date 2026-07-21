import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(page_title="SharpPLAY Analytics Terminal", layout="wide")

# Custom Dark Theme Styling & Terminal UI
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0c10;
        color: #ffffff;
    }
    .terminal-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin-bottom: 5px;
    }
    .terminal-sub {
        font-size: 0.9rem;
        color: #9ba1a6;
        text-align: center;
        margin-bottom: 15px;
    }
    .section-title {
        font-size: 1.15rem;
        font-weight: 600;
        color: #00ffcc;
        margin-top: 20px;
        margin-bottom: 8px;
    }
    .card-box {
        background-color: #12141a;
        border: 1px solid #222632;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .stButton > button {
        width: 100%;
        background-color: #161b22;
        color: #00ffcc;
        border: 1px solid #00ffcc;
        border-radius: 8px;
        font-weight: 600;
        padding: 10px;
        margin-top: 5px;
    }
    .stButton > button:hover {
        background-color: #00ffcc;
        color: #0b0c10;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="terminal-header">⚾ SharpPLAY: Lineup & Analytics Terminal</div>', unsafe_allow_html=True)
st.markdown('<div class="terminal-sub">Tap a game below to load lineups, weather impact, and batter pitch-mix metrics</div>', unsafe_allow_html=True)

# Initialize Session State
if "selected_matchup" not in st.session_state:
    st.session_state.selected_matchup = "Washington Nationals @ Colorado Rockies"

# Game Slate Data Dictionary
slate_games = {
    "Washington Nationals @ Colorado Rockies": {
        "time": "8:40 PM EDT", "weather": "84°F | Wind 12 mph Out to CF", "grade": "BOOSTED +18% (A+)", "away": "Washington Nationals", "home": "Colorado Rockies"
    },
    "San Diego Padres @ Atlanta Braves": {
        "time": "BOT 5th", "weather": "72°F | Wind 8 mph In", "grade": "Neutral (C)", "away": "San Diego Padres", "home": "Atlanta Braves"
    },
    "New York Mets @ Milwaukee Brewers": {
        "time": "TOP 3RD", "weather": "Dome (Closed)", "grade": "Neutral (C)", "away": "New York Mets", "home": "Milwaukee Brewers"
    },
    "Cincinnati Reds @ Seattle Mariners": {
        "time": "9:40 PM EDT", "weather": "58°F | Wind 11 mph In", "grade": "SUPPRESSED -12% (D)", "away": "Cincinnati Reds", "home": "Seattle Mariners"
    },
    "Boston Red Sox @ New York Yankees": {
        "time": "7:05 PM EDT", "weather": "78°F | Wind 9 mph Out to RF", "grade": "BOOSTED +8% (B+)", "away": "Boston Red Sox", "home": "New York Yankees"
    },
    "Los Angeles Dodgers @ San Francisco Giants": {
        "time": "10:10 PM EDT", "weather": "55°F | Wind 14 mph Out from Bay", "grade": "SUPPRESSED -15% (D-)", "away": "Los Angeles Dodgers", "home": "San Francisco Giants"
    }
}

st.markdown('<div class="section-title">📅 Tap Game to Load Analytics</div>', unsafe_allow_html=True)

for matchup_key, info in slate_games.items():
    is_active = (st.session_state.selected_matchup == matchup_key)
    btn_label = f"{'🟢 [ACTIVE] ' if is_active else '⚡ '}{matchup_key} ({info['time']}) | 🌤️ {info['weather']} | Grade: {info['grade']}"
    
    if st.button(btn_label, key=f"game_btn_{matchup_key}"):
        st.session_state.selected_matchup = matchup_key
        st.rerun()

current_game_info = slate_games[st.session_state.selected_matchup]
away_team = current_game_info["away"]
home_team = current_game_info["home"]

st.markdown("---")
st.markdown(f"""
<div class="card-box" style="border-color: #00ffcc;">
    <h3 style="margin: 0; color: #00ffcc;">⚡ Active Analysis: {st.session_state.selected_matchup}</h3>
    <p style="margin: 5px 0 0 0; color: #ccc;">🌤️ Weather Conditions: {current_game_info['weather']} &nbsp;|&nbsp; <b>Weather Grade: {current_game_info['grade']}</b></p>
</div>
""", unsafe_allow_html=True)

# FULL TEAM LINEUP METRICS SECTION
col_away_lineup, col_home_lineup = st.columns(2)

with col_away_lineup:
    st.markdown(f'<div class="section-title">🔴 {away_team} Lineup & Metrics</div>', unsafe_allow_html=True)
    away_lineup_data = [
        {"Bat": "1. C. Carrigg (CF)", "AVG": ".285", "OBP": ".350", "SLG": ".480", "wOBA": ".362", "ISO": ".195", "Hard%": "42.1%"},
        {"Bat": "2. J. Wood (LF)", "AVG": ".272", "OBP": ".345", "SLG": ".510", "wOBA": ".375", "ISO": ".238", "Hard%": "48.6%"},
        {"Bat": "3. C. Crews (RF)", "AVG": ".265", "OBP": ".330", "SLG": ".460", "wOBA": ".348", "ISO": ".195", "Hard%": "40.2%"},
        {"Bat": "4. N. Schuelke (1B)", "AVG": ".250", "OBP": ".320", "SLG": ".440", "wOBA": ".332", "ISO": ".190", "Hard%": "39.0%"},
        {"Bat": "5. L. Garcia (2B)", "AVG": ".278", "OBP": ".315", "SLG": ".410", "wOBA": ".325", "ISO": ".132", "Hard%": "35.4%"},
        {"Bat": "6. I. Tena (3B)", "AVG": ".245", "OBP": ".300", "SLG": ".390", "wOBA": ".305", "ISO": ".145", "Hard%": "34.1%"},
        {"Bat": "7. CJ Abrams (SS)", "AVG": ".260", "OBP": ".310", "SLG": ".450", "wOBA": ".335", "ISO": ".190", "Hard%": "41.0%"},
        {"Bat": "8. K. Ruiz (C)", "AVG": ".240", "OBP": ".280", "SLG": ".370", "wOBA": ".285", "ISO": ".130", "Hard%": "31.2%"},
        {"Bat": "9. T. Lipscomb (DH)", "AVG": ".235", "OBP": ".290", "SLG": ".380", "wOBA": ".295", "ISO": ".145", "Hard%": "33.5%"}
    ]
    df_away = pd.DataFrame(away_lineup_data)
    st.dataframe(df_away, use_container_width=True, hide_index=True)

with col_home_lineup:
    st.markdown(f'<div class="section-title">🔵 {home_team} Lineup & Metrics</div>', unsafe_allow_html=True)
    home_lineup_data = [
        {"Bat": "1. E. Tovar (SS)", "AVG": ".275", "OBP": ".320", "SLG": ".455", "wOBA": ".340", "ISO": ".180", "Hard%": "43.2%"},
        {"Bat": "2. R. McMahon (3B)", "AVG": ".258", "OBP": ".342", "SLG": ".470", "wOBA": ".352", "ISO": ".212", "Hard%": "45.0%"},
        {"Bat": "3. B. Doyle (CF)", "AVG": ".268", "OBP": ".315", "SLG": ".465", "wOBA": ".345", "ISO": ".197", "Hard%": "46.2%"},
        {"Bat": "4. E. Montero (1B)", "AVG": ".250", "OBP": ".300", "SLG": ".430", "wOBA": ".320", "ISO": ".180", "Hard%": "38.5%"},
        {"Bat": "5. H. Goodman (C)", "AVG": ".242", "OBP": ".285", "SLG": ".420", "wOBA": ".310", "ISO": ".178", "Hard%": "40.1%"},
        {"Bat": "6. N. Jones (RF)", "AVG": ".255", "OBP": ".325", "SLG": ".410", "wOBA": ".325", "ISO": ".155", "Hard%": "36.8%"},
        {"Bat": "7. S. Bouchard (LF)", "AVG": ".238", "OBP": ".310", "SLG": ".390", "wOBA": ".308", "ISO": ".152", "Hard%": "35.0%"},
        {"Bat": "8. A. Trejo (2B)", "AVG": ".245", "OBP": ".295", "SLG": ".360", "wOBA": ".290", "ISO": ".115", "Hard%": "30.4%"},
        {"Bat": "9. P. Severino (DH)", "AVG": ".230", "OBP": ".280", "SLG": ".375", "wOBA": ".288", "ISO": ".145", "Hard%": "32.0%"}
    ]
    df_home = pd.DataFrame(home_lineup_data)
    st.dataframe(df_home, use_container_width=True, hide_index=True)

st.markdown("---")

# INTERACTIVE BATTER VS PITCH MIX SECTION
st.markdown('<div class="section-title">🔍 Batter vs. Pitch Mix Performance Lookup</div>', unsafe_allow_html=True)

# Combine all players from both teams into a single list for selection
all_batters = [row["Bat"] for row in away_lineup_data] + [row["Bat"] for row in home_lineup_data]

selected_batter = st.selectbox("Select Batter to Analyze vs Pitch Mix:", options=all_batters)

# Mock sample pitch-mix data generator based on selected batter
pitch_mix_breakdown = [
    {"Pitch Type": "4-Seam Fastball", "Usage%": "42%", "BA": ".295", "SLG": ".530", "wOBA": ".385", "Whiff%": "21.4%"},
    {"Pitch Type": "Slider / Sweeper", "Usage%": "28%", "BA": ".230", "SLG": ".390", "wOBA": ".302", "Whiff%": "34.2%"},
    {"Pitch Type": "Curveball", "Usage%": "15%", "BA": ".215", "SLG": ".350", "wOBA": ".280", "Whiff%": "38.9%"},
    {"Pitch Type": "Changeup / Splitter", "Usage%": "15%", "BA": ".270", "SLG": ".440", "wOBA": ".340", "Whiff%": "24.5%"}
]

st.markdown(f"<p style='color: #00ffcc; font-weight: 600;'>Performance Breakdown for {selected_batter}:</p>", unsafe_allow_html=True)
df_pitch_mix = pd.DataFrame(pitch_mix_breakdown)
st.dataframe(df_pitch_mix, use_container_width=True, hide_index=True)

st.markdown("---")

# STARTING PITCHER MATCHUP COMPARISON
st.markdown('<div class="section-title">🎯 Starting Pitcher Matchup Breakdown</div>', unsafe_allow_html=True)
p_cols = st.columns(2)
with p_cols[0]:
    st.markdown(f"""
    <div class="card-box">
        <h4 style="color: #00ffcc; margin-top:0;">Away Starter ({away_team})</h4>
        <p style="color: #9ba1a6; font-size: 0.85rem; margin-bottom: 5px;">ERA: 3.84 | WHIP: 1.22 | K/9: 8.9 | FIP: 4.10</p>
        <p style="font-size: 0.85rem;"><b>Pitch Arsenal:</b> 4-Seam (45%), Curveball (30%), Slider (15%), Sinker (10%)</p>
    </div>
    """, unsafe_allow_html=True)
with p_cols[1]:
    st.markdown(f"""
    <div class="card-box">
        <h4 style="color: #00ffcc; margin-top:0;">Home Starter ({home_team})</h4>
        <p style="color: #9ba1a6; font-size: 0.85rem; margin-bottom: 5px;">ERA: 4.45 | WHIP: 1.34 | K/9: 8.2 | FIP: 4.35</p>
        <p style="font-size: 0.85rem;"><b>Pitch Arsenal:</b> Fastball (42%), Slider (28%), Changeup (18%), Curveball (12%)</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<p style='color: #555960; text-align: center; font-size: 0.8rem; margin-top: 30px;'>doinksports.com • SharpPLAY Analytics Terminal</p>", unsafe_allow_html=True)
