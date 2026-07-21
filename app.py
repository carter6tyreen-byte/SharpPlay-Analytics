import streamlit as st
import pandas as pd
import os

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
st.markdown('<div class="terminal-sub">Color-coded matchup board showing batter performance vs. starting pitcher pitch mix</div>', unsafe_allow_html=True)

# Initialize Session State
if "selected_matchup" not in st.session_state:
    st.session_state.selected_matchup = "Washington Nationals @ Colorado Rockies"

slate_games = {
    "Washington Nationals @ Colorado Rockies": {
        "time": "8:40 PM EDT", "weather": "84°F | Wind 12 mph Out to CF", "grade": "BOOSTED +18% (A+)", "away": "Washington Nationals", "home": "Colorado Rockies",
        "away_win_prob": "58.4%", "home_win_prob": "41.6%", "model_edge": "Washington Nationals (-135)",
        "away_pitcher": "S. Freeland (LHP)", "away_arsenal": "Fastball 44% | Slider 28% | Changeup 18%",
        "home_pitcher": "M. Gore (LHP)", "home_arsenal": "4-Seam 48% | Curveball 26% | Changeup 16%", "status": "Upcoming"
    },
    "San Diego Padres @ Atlanta Braves": {
        "time": "BOT 5th", "weather": "72°F | Wind 8 mph In", "grade": "Neutral (C)", "away": "San Diego Padres", "home": "Atlanta Braves",
        "away_win_prob": "48.2%", "home_win_prob": "51.8%", "model_edge": "Atlanta Braves (-110)",
        "away_pitcher": "M. King (RHP)", "away_arsenal": "Sinker 42% | Sweeper 30% | Changeup 18%",
        "home_pitcher": "C. Sale (LHP)", "home_arsenal": "4-Seam 52% | Slider 32% | Changeup 16%", "status": "Live"
    }
}

st.markdown('<div class="section-title">📅 Slate & Filter Options</div>', unsafe_allow_html=True)
filter_mode = st.radio("Filter Slate", ["All Games", "🌟 A+ Boosted Only", "⚡ Live Games Only"], horizontal=True, label_visibility="collapsed")

st.markdown('<div class="section-title">Tap Game to Load Analytics</div>', unsafe_allow_html=True)

filtered_games = {}
for matchup_key, info in slate_games.items():
    if filter_mode == "🌟 A+ Boosted Only" and "A+" not in info["grade"]:
        continue
    if filter_mode == "⚡ Live Games Only" and info["status"] != "Live":
        continue
    filtered_games[matchup_key] = info

if not filtered_games:
    st.info("No games match the current filter selection.")
else:
    for matchup_key, info in filtered_games.items():
        is_active = (st.session_state.selected_matchup == matchup_key)
        btn_label = f"{'🟢 [ACTIVE] ' if is_active else '⚡ '}{matchup_key} ({info['time']}) | Win Prob: {info['away']} {info['away_win_prob']} / {info['home']} {info['home_win_prob']}"
        
        if st.button(btn_label, key=f"game_btn_{matchup_key}"):
            st.session_state.selected_matchup = matchup_key
            st.rerun()

if st.session_state.selected_matchup not in slate_games:
    st.session_state.selected_matchup = list(slate_games.keys())[0]

current_game_info = slate_games[st.session_state.selected_matchup]
away_team, home_team = current_game_info["away"], current_game_info["home"]

st.markdown("---")
st.markdown(f"""
<div class="card-box" style="border-color: #00ffcc;">
    <h3 style="margin: 0; color: #00ffcc;">⚡ Active Prediction & Analysis: {st.session_state.selected_matchup}</h3>
    <p style="margin: 8px 0 0 0; color: #fff;"><b>Model Win Probabilities:</b> {away_team} ({current_game_info['away_win_prob']}) vs {home_team} ({current_game_info['home_win_prob']})</p>
    <p style="margin: 4px 0 0 0; color: #00ffcc;"><b>Recommended Model Edge:</b> {current_game_info['model_edge']} &nbsp;|&nbsp; Weather Grade: {current_game_info['grade']}</p>
</div>
""", unsafe_allow_html=True)

def color_matchup_grade(val):
    if any(tag in str(val) for tag in ["🟢", "A+", "A", "B+", ".36", ".37", ".38", ".5"]):
        return 'background-color: #0d2818; color: #2ecc71; font-weight: 600;'
    elif any(tag in str(val) for tag in ["🔴", "D", "F", ".28", ".29", ".30", ".31"]):
        return 'background-color: #381313; color: #e74c3c; font-weight: 600;'
    return ''

col_away_lineup, col_home_lineup = st.columns(2)

with col_away_lineup:
    st.markdown(f'<div class="section-title">🔴 {away_team} Lineup</div>', unsafe_allow_html=True)
    away_lineup_data = [
        {"Bat": "1. C. Carrigg (CF)", "Matchup": "🟢 Elite (.385 wOBA)", "AVG": ".285", "SLG": ".480", "wOBA": ".362", "Hard%": "42.1%"},
        {"Bat": "2. J. Wood (LF)", "Matchup": "🟢 Elite (.410 wOBA)", "AVG": ".272", "SLG": ".510", "wOBA": ".375", "Hard%": "48.6%"},
        {"Bat": "3. C. Crews (RF)", "Matchup": "🟢 Good (.350 wOBA)", "AVG": ".265", "SLG": ".460", "wOBA": ".348", "Hard%": "40.2%"}
    ]
    df_away = pd.DataFrame(away_lineup_data)
    styled_away = df_away.style.map(color_matchup_grade, subset=['Matchup', 'wOBA'])
    st.dataframe(styled_away, use_container_width=True, hide_index=True)

with col_home_lineup:
    st.markdown(f'<div class="section-title">🔵 {home_team} Lineup</div>', unsafe_allow_html=True)
    home_lineup_data = [
        {"Bat": "1. E. Tovar (SS)", "Matchup": "🟢 Good (.345 wOBA)", "AVG": ".275", "SLG": ".455", "wOBA": ".340", "Hard%": "43.2%"},
        {"Bat": "2. R. McMahon (3B)", "Matchup": "🟢 Elite (.390 wOBA)", "AVG": ".258", "SLG": ".470", "wOBA": ".352", "Hard%": "45.0%"},
        {"Bat": "3. B. Doyle (CF)", "Matchup": "🟢 Elite (.380 wOBA)", "AVG": ".268", "SLG": ".465", "wOBA": ".345", "Hard%": "46.2%"}
    ]
    df_home = pd.DataFrame(home_lineup_data)
    styled_home = df_home.style.map(color_matchup_grade, subset=['Matchup', 'wOBA'])
    st.dataframe(styled_home, use_container_width=True, hide_index=True)

# FULL-VIEW PITCHER ARSENAL & MATCHUP MATRIX (No dropdowns needed!)
st.markdown("---")
st.markdown('<div class="section-title">🎯 Starting Pitcher Arsenals & Full Matchup Breakdown</div>', unsafe_allow_html=True)

col_pitcher_1, col_pitcher_2 = st.columns(2)
with col_pitcher_1:
    st.markdown(f"""
    <div class="card-box">
        <h4 style="margin: 0; color: #00ffcc;">{away_team} Pitcher</h4>
        <p style="margin: 4px 0 8px 0; font-size: 0.9rem;"><b>{current_game_info['away_pitcher']}</b></p>
        <p style="margin: 0; color: #ccc; font-size: 0.85rem;"><b>Arsenal:</b> {current_game_info['away_arsenal']}</p>
    </div>
    """, unsafe_allow_html=True)

with col_pitcher_2:
    st.markdown(f"""
    <div class="card-box">
        <h4 style="margin: 0; color: #00ffcc;">{home_team} Pitcher</h4>
        <p style="margin: 4px 0 8px 0; font-size: 0.9rem;"><b>{current_game_info['home_pitcher']}</b></p>
        <p style="margin: 0; color: #ccc; font-size: 0.85rem;"><b>Arsenal:</b> {current_game_info['home_arsenal']}</p>
    </div>
    """, unsafe_allow_html=True)

# Comprehensive visible breakdown table for all key hitters
st.markdown('<p style="color: #9ba1a6; font-size: 0.9rem; margin-top: 15px;"><b>Full Slate Arsenal Vulnerability & Matchup Matrix:</b></p>', unsafe_allow_html=True)

matrix_data = [
    {"Hitter": "C. Carrigg (CF)", "Team": away_team, "Primary Threat": "Fastball Damage", "Vulnerability": "Low-Away Breaking", "Verdict": "🟢 Favorable Edge"},
    {"Hitter": "J. Wood (LF)", "Team": away_team, "Primary Threat": "Elite Exit Velocity", "Vulnerability": "High Heat", "Verdict": "🟢 Massive Edge"},
    {"Hitter": "C. Crews (RF)", "Team": away_team, "Primary Threat": "Line Drive Rate", "Vulnerability": "Changeup Chase", "Verdict": "🟡 Neutral"},
    {"Hitter": "E. Tovar (SS)", "Team": home_team, "Primary Threat": "Contact Consistency", "Vulnerability": "Sliders Away", "Verdict": "🟢 Favorable Edge"},
    {"Hitter": "R. McMahon (3B)", "Team": home_team, "Primary Threat": "Power / Hard%", "Vulnerability": "LHP Fastballs", "Verdict": "🟢 Elite Edge"},
    {"Hitter": "B. Doyle (CF)", "Team": home_team, "Primary Threat": "Speed & Gap Power", "Vulnerability": "Breaking Balls", "Verdict": "🟢 Favorable Edge"}
]

df_matrix = pd.DataFrame(matrix_data)
st.dataframe(df_matrix, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("<p style='color: #555960; text-align: center; font-size: 0.8rem;'>doinksports.com • SharpPLAY Analytics Terminal</p>", unsafe_allow_html=True)
