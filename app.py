import streamlit as st
import statsapi
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(page_title="SharpPLAY Analytics - Batter vs Pitcher Terminal", layout="wide")

# Custom Dark Theme Styling matching Professional Terminal UI with Green/Red conditional highlights & Doink Sports Inspired Layout
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
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .selection-box {
        background-color: #12141a;
        border: 1px solid #222632;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin-bottom: 15px;
    }
    .badge-green {
        background-color: #1e4620;
        color: #00ffcc;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    .badge-red {
        background-color: #4a1525;
        color: #ff4d4d;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    .badge-yellow {
        background-color: #4d4315;
        color: #ffcc00;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
    }
    .tab-container {
        display: flex;
        gap: 8px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="terminal-header">⚾ SharpPLAY: Batter vs. Pitcher Deep-Dive Terminal</div>', unsafe_allow_html=True)
st.markdown('<div class="terminal-sub">Advanced Pitch-Level Breakdown, Statcast Metrics, and Green/Red Performance Matrix</div>', unsafe_allow_html=True)

# Initialize Session State
today_str = datetime.now().strftime("%m/%d/%Y")
if "query_date" not in st.session_state:
    st.session_state.query_date = today_str

# Top Navigation Tabs (matching Doink Sports style inspiration)
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)
with nav_col1:
    st.markdown('<div class="selection-box" style="border-color: #00ffcc; padding: 10px;"><b style="color: #00ffcc;">Batter vs Pitcher</b></div>', unsafe_allow_html=True)
with nav_col2:
    st.markdown('<div class="selection-box" style="padding: 10px; color: #9ba1a6;">Weather Man</div>', unsafe_allow_html=True)
with nav_col3:
    st.markdown('<div class="selection-box" style="padding: 10px; color: #9ba1a6;">Hit Rater</div>', unsafe_allow_html=True)
with nav_col4:
    st.markdown('<div class="selection-box" style="padding: 10px; color: #9ba1a6;">Trending Insights</div>', unsafe_allow_html=True)

# Live Slate / Game Selector Bar
st.markdown("<p style='color: #9ba1a6; font-size: 0.85rem; margin-bottom: 5px;'>SELECT GAME FROM SLATE</p>", unsafe_allow_html=True)
game_cols = st.columns(4)
with game_cols[0]:
    st.markdown('<div class="selection-box" style="padding: 10px; font-size: 0.85rem; border-left: 3px solid #ff4d4d;">BOT 5TH<br><b>San Diego</b><br>Atlanta</div>', unsafe_allow_html=True)
with game_cols[1]:
    st.markdown('<div class="selection-box" style="padding: 10px; font-size: 0.85rem; border-left: 3px solid #ff4d4d;">TOP 3RD<br><b>New York</b><br>Milwaukee</div>', unsafe_allow_html=True)
with game_cols[2]:
    st.markdown('<div class="selection-box" style="padding: 10px; font-size: 0.85rem; border-left: 3px solid #ffcc00;">8:40 PM<br><b>Washington</b><br>Colorado</div>', unsafe_allow_html=True)
with game_cols[3]:
    st.markdown('<div class="selection-box" style="padding: 10px; font-size: 0.85rem; border-left: 3px solid #2b2f3a;">9:40 PM<br><b>Cincinnati</b><br>Seattle</div>', unsafe_allow_html=True)

st.markdown("---")

# BATTER & PITCHER SELECTION CARDS
col_bat, col_pit = st.columns(2)

with col_bat:
    st.markdown("""
    <div class="selection-box">
        <h4 style="color: #9ba1a6; margin-top: 0; font-size: 0.9rem;">BATTER</h4>
        <h3>Cole Carrigg</h3>
        <p style="color: #9ba1a6; font-size: 0.85rem; margin-bottom: 0;">COL | SW | CF</p>
    </div>
    """, unsafe_allow_html=True)

with col_pit:
    st.markdown("""
    <div class="selection-box">
        <h4 style="color: #9ba1a6; margin-top: 0; font-size: 0.9rem;">PITCHER</h4>
        <h3>Andrew Alvarez</h3>
        <p style="color: #9ba1a6; font-size: 0.85rem; margin-bottom: 0;">WSH | LHP</p>
    </div>
    """, unsafe_allow_html=True)

# Summary Matchup Stat Bar
sc_cols = st.columns(5)
with sc_cols[0]:
    st.markdown('<div class="selection-box" style="padding: 10px;"><span style="color: #9ba1a6; font-size: 0.8rem;">PA</span><br><b>0</b></div>', unsafe_allow_html=True)
with sc_cols[1]:
    st.markdown('<div class="selection-box" style="padding: 10px;"><span style="color: #9ba1a6; font-size: 0.8rem;">AVG</span><br><b>--</b></div>', unsafe_allow_html=True)
with sc_cols[2]:
    st.markdown('<div class="selection-box" style="padding: 10px;"><span style="color: #9ba1a6; font-size: 0.8rem;">SLG</span><br><b>--</b></div>', unsafe_allow_html=True)
with sc_cols[3]:
    st.markdown('<div class="selection-box" style="padding: 10px;"><span style="color: #9ba1a6; font-size: 0.8rem;">WOBA</span><br><b>--</b></div>', unsafe_allow_html=True)
with sc_cols[4]:
    st.markdown('<div class="selection-box" style="padding: 10px;"><span style="color: #9ba1a6; font-size: 0.8rem;">HR</span><br><b>--</b></div>', unsafe_allow_html=True)

st.markdown("---")

# PITCHER DEEP DIVE SECTION (Andrew Alvarez - vs RHB / 2026)
st.markdown('<div class="section-title">🔴 Andrew Alvarez (WSH | LHP) — Pitch-by-Pitch Breakdown (2026 vs RHB)</div>', unsafe_allow_html=True)

pitcher_data = [
    {"Pitch": "🔵 Four-seam FB", "AB": "42", "AVG": ".286", "SLG": ".452", "ISO": ".167", "H": "12", "HR": "1", "BRL%": "11.1%", "HH%": "30.6%", "EV": "87.2"},
    {"Pitch": "🟠 Curveball", "AB": "52", "AVG": ".154", "SLG": ".231", "ISO": ".077", "H": "8", "HR": "0", "BRL%": "0.0%", "HH%": "59.1%", "EV": "88.2"},
    {"Pitch": "🔴 Slider", "AB": "21", "AVG": ".333", "SLG": ".476", "ISO": ".143", "H": "7", "HR": "0", "BRL%": "12.5%", "HH%": "50.0%", "EV": "91.4"},
    {"Pitch": "🟠 Sinker", "AB": "11", "AVG": ".455", "SLG": ".455", "ISO": ".000", "H": "5", "HR": "0", "BRL%": "9.1%", "HH%": "54.5%", "EV": "86.7"},
    {"Pitch": "🔵 Changeup", "AB": "4", "AVG": ".250", "SLG": ".250", "ISO": ".000", "H": "1", "HR": "0", "BRL%": "0.0%", "HH%": "0.0%", "EV": "74.2"},
]

df_pit = pd.DataFrame(pitcher_data)

def color_code_metrics(val):
    if val in [".154", ".231", ".077", "0", "0.0%"]:
        return 'background-color: #1e4620; color: #00ffcc;'
    elif val in [".333", ".476", ".455", ".286", ".452", "12.5%", "50.0%", "91.4", "1"]:
        return 'background-color: #4a1525; color: #ff4d4d;'
    return 'background-color: #12141a; color: #ffffff;'

st.dataframe(df_pit.style.applymap(color_code_metrics, subset=['AVG', 'SLG', 'ISO', 'HR', 'BRL%', 'HH%']), use_container_width=True, hide_index=True)

st.markdown("---")

# BATTER DEEP DIVE SECTION (Cole Carrigg - vs LHP / 2026)
st.markdown('<div class="section-title">🟢 Cole Carrigg (COL | SW) — Pitch-by-Pitch Breakdown (2026 vs LHP)</div>', unsafe_allow_html=True)

batter_data = [
    {"Pitch": "🔵 Four-seam FB", "AB": "15", "AVG": ".267", "SLG": ".467", "ISO": ".200", "H": "4", "HR": "1", "BRL%": "9.1%", "HH%": "18.2%", "EV": "81.4"},
    {"Pitch": "🔴 Slider", "AB": "10", "AVG": ".500", "SLG": ".800", "ISO": ".300", "H": "5", "HR": "0", "BRL%": "12.5%", "HH%": "37.5%", "EV": "77.3"},
    {"Pitch": "🟠 Sinker", "AB": "9", "AVG": ".222", "SLG": ".222", "ISO": ".000", "H": "2", "HR": "0", "BRL%": "0.0%", "HH%": "30.0%", "EV": "83.5"},
    {"Pitch": "🔵 Changeup", "AB": "8", "AVG": ".375", "SLG": ".750", "ISO": ".375", "H": "3", "HR": "1", "BRL%": "33.3%", "HH%": "66.7%", "EV": "86.1"},
    {"Pitch": "🟠 Curveball", "AB": "2", "AVG": ".000", "SLG": ".000", "ISO": ".000", "H": "0", "HR": "0", "BRL%": "--", "HH%": "--", "EV": "--"},
]

df_bat = pd.DataFrame(batter_data)
st.dataframe(df_bat.style.applymap(color_code_metrics, subset=['AVG', 'SLG', 'ISO', 'HR', 'BRL%', 'HH%']), use_container_width=True, hide_index=True)

st.markdown("---")

# PA LOGS SECTION
st.markdown('<div class="section-title">📋 PA Logs</div>', unsafe_allow_html=True)
st.markdown("<p style='color: #9ba1a6; font-size: 0.85rem;'>Each PA between batter and pitcher since 2020</p>", unsafe_allow_html=True)
st.markdown("""
<div class="selection-box" style="padding: 30px; color: #9ba1a6;">
    Select a batter and pitcher to view plate appearances.
</div>
""", unsafe_allow_html=True)

st.markdown("<p style='color: #555960; text-align: center; font-size: 0.8rem; margin-top: 30px;'>doinksports.com • SharpPLAY Analytics Terminal</p>", unsafe_allow_html=True)
