import streamlit as st
import statsapi
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
        font-size: 1.6rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin-bottom: 5px;
    }
    .terminal-sub {
        font-size: 0.95rem;
        color: #9ba1a6;
        text-align: center;
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #00ffcc;
        margin-top: 25px;
        margin-bottom: 10px;
    }
    .card-box {
        background-color: #12141a;
        border: 1px solid #222632;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="terminal-header">⚾ SharpPLAY: Full Slate & Lineup Analytics Terminal</div>', unsafe_allow_html=True)
st.markdown('<div class="terminal-sub">Live Game Selector, Weather Impact Ratings, and Full Team Lineup Breakdowns</div>', unsafe_allow_html=True)

# Initialize Session State for active game selection
if "selected_game" not in st.session_state:
    st.session_state.selected_game = "Washington Nationals @ Colorado Rockies"

# Top Navigation Tabs
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
with nav_col1:
    st.markdown('<div class="card-box" style="border-color: #00ffcc; text-align: center;"><b style="color: #00ffcc;">Matchups & Lineups</b></div>', unsafe_allow_html=True)
with nav_col2:
    st.markdown('<div class="card-box" style="text-align: center; color: #9ba1a6;">Weather Man</div>', unsafe_allow_html=True)
with nav_col3:
    st.markdown('<div class="card-box" style="text-align: center; color: #9ba1a6;">Hit Rater</div>', unsafe_allow_html=True)
with nav_col4:
    st.markdown('<div class="card-box" style="text-align: center; color: #9ba1a6;">Trending Insights</div>', unsafe_allow_html=True)

st.markdown("---")

# FULL SLATE & WEATHER IMPACT SELECTOR
st.markdown('<div class="section-title">📅 Today\'s Full Game Slate & Weather Impact Grades</div>', unsafe_allow_html=True)
st.markdown("<p style='color: #9ba1a6; font-size: 0.85rem;'>Click a game below to load full team lineups and pitcher metrics.</p>", unsafe_allow_html=True)

# Comprehensive game slate data with weather impact ratings
slate_games = [
    {"matchup": "San Diego Padres @ Atlanta Braves", "time": "Final (BOT 5th)", "weather": "72°F | Wind 8 mph In", "grade": "Neutral (C)", "color": "#ff4d4d"},
    {"matchup": "New York Mets @ Milwaukee Brewers", "time": "Live (TOP 3RD)", "weather": "Dome (Closed)", "grade": "Neutral (C)", "color": "#ff4d4d"},
    {"matchup": "Washington Nationals @ Colorado Rockies", "time": "8:40 PM EDT", "weather": "84°F | Wind 12 mph Out to CF", "grade": "BOOSTED +18% (A+)", "color": "#00ffcc"},
    {"matchup": "Cincinnati Reds @ Seattle Mariners", "time": "9:40 PM EDT", "weather": "58°F | Wind 11 mph In", "grade": "SUPPRESSED -12% (D)", "color": "#ffcc00"},
    {"matchup": "Boston Red Sox @ New York Yankees", "time": "7:05 PM EDT", "weather": "78°F | Wind 9 mph Out to RF", "grade": "BOOSTED +8% (B+)", "color": "#00ffcc"},
    {"matchup": "Los Angeles Dodgers @ San Francisco Giants", "time": "10:10 PM EDT", "weather": "55°F | Wind 14 mph Out from Bay", "grade": "SUPPRESSED -15% (D-)", "color": "#ffcc00"}
]

cols = st.columns(3)
for i, g in enumerate(slate_games):
    with cols[i % 3]:
        is_selected = (st.session_state.selected_game == g["matchup"])
        border_col = "#00ffcc" if is_selected else "#222632"
        bg_col = "#1a2130" if is_selected else "#12141a"
        
        st.markdown(f"""
        <div style="background-color: {bg_col}; border: 2px solid {border_col}; border-radius: 10px; padding: 12px; margin-bottom: 10px;">
            <span style="font-size: 0.75rem; color: #9ba1a6;">{g['time']}</span><br>
            <b style="font-size: 0.95rem;">{g['matchup']}</b><br>
            <span style="font-size: 0.8rem; color: #ccc;">🌤️ {g['weather']}</span><br>
            <span style="font-size: 0.8rem; font-weight: bold; color: {g['color']};">⚡ Weather Grade: {g['grade']}</span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"Load Matchup", key=f"btn_{i} ({g['matchup']})"):
            st.session_state.selected_game = g["matchup"]
            st.rerun()

st.markdown("---")
st.markdown(f"### ⚡ Active Analysis: <span style='color: #00ffcc;'>{st.session_state.selected_game}</span>", unsafe_allow_html=True)

# FULL TEAM LINEUP METRICS SECTION
col_away_lineup, col_home_lineup = st.columns(2)

away_team, home_team = st.session_state.selected_game.split(" @ ")

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

# STARTING PITCHER MATCHUP COMPARISON
st.markdown('<div class="section-title">🎯 Starting Pitcher Matchup Breakdown</div>', unsafe_allow_html=True)
p_cols = st.columns(2)
with p_cols[0]:
    st.markdown("""
    <div class="card-box">
        <h4 style="color: #00ffcc; margin-top:0;">Away Starter: Andrew Alvarez (LHP)</h4>
        <p style="color: #9ba1a6; font-size: 0.85rem; margin-bottom: 5px;">ERA: 3.84 | WHIP: 1.22 | K/9: 8.9 | FIP: 4.10</p>
        <p style="font-size: 0.85rem;"><b>Pitch Arsenal:</b> 4-Seam (45%), Curveball (30%), Slider (15%), Sinker (10%)</p>
    </div>
    """, unsafe_allow_html=True)
with p_cols[1]:
    st.markdown("""
    <div class="card-box">
        <h4 style="color: #00ffcc; margin-top:0;">Home Starter: Ryan Feltner (RHP)</h4>
        <p style="color: #9ba1a6; font-size: 0.85rem; margin-bottom: 5px;">ERA: 4.45 | WHIP: 1.34 | K/9: 8.2 | FIP: 4.35</p>
        <p style="font-size: 0.85rem;"><b>Pitch Arsenal:</b> Fastball (42%), Slider (28%), Changeup (18%), Curveball (12%)</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<p style='color: #555960; text-align: center; font-size: 0.8rem; margin-top: 30px;'>doinksports.com • SharpPLAY Analytics Terminal</p>", unsafe_allow_html=True)
