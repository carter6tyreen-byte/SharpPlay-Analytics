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
st.markdown('<div class="terminal-sub">Color-coded matchup board showing batter performance vs. starting pitcher pitch mix</div>', unsafe_allow_html=True)

# Initialize Session State
if "selected_matchup" not in st.session_state:
    st.session_state.selected_matchup = "Washington Nationals @ Colorado Rockies"

# Game Slate Data Dictionary with Detailed Pitcher Arsenals
slate_games = {
    "Washington Nationals @ Colorado Rockies": {
        "time": "8:40 PM EDT", "weather": "84°F | Wind 12 mph Out to CF", "grade": "BOOSTED +18% (A+)", "away": "Washington Nationals", "home": "Colorado Rockies",
        "away_arsenal": {"4-Seam Fastball": "45%", "Curveball": "30%", "Slider": "15%", "Sinker": "10%"},
        "home_arsenal": {"Fastball": "42%", "Slider": "28%", "Changeup": "18%", "Curveball": "12%"}
    },
    "San Diego Padres @ Atlanta Braves": {
        "time": "BOT 5th", "weather": "72°F | Wind 8 mph In", "grade": "Neutral (C)", "away": "San Diego Padres", "home": "Atlanta Braves",
        "away_arsenal": {"Sinker": "40%", "Slider": "30%", "Changeup": "20%", "4-Seam Fastball": "10%"},
        "home_arsenal": {"4-Seam Fastball": "50%", "Slider": "25%", "Splitter": "15%", "Curveball": "10%"}
    },
    "New York Mets @ Milwaukee Brewers": {
        "time": "TOP 3RD", "weather": "Dome (Closed)", "grade": "Neutral (C)", "away": "New York Mets", "home": "Milwaukee Brewers",
        "away_arsenal": {"4-Seam Fastball": "48%", "Sweeper": "25%", "Splitter": "17%", "Curveball": "10%"},
        "home_arsenal": {"Sinker": "42%", "Slider": "32%", "Changeup": "16%", "Curveball": "10%"}
    },
    "Cincinnati Reds @ Seattle Mariners": {
        "time": "9:40 PM EDT", "weather": "58°F | Wind 11 mph In", "grade": "SUPPRESSED -12% (D)", "away": "Cincinnati Reds", "home": "Seattle Mariners",
        "away_arsenal": {"Fastball": "44%", "Slider": "30%", "Curveball": "16%", "Changeup": "10%"},
        "home_arsenal": {"4-Seam Fastball": "52%", "Sweeper": "26%", "Sinker": "12%", "Curveball": "10%"}
    },
    "Boston Red Sox @ New York Yankees": {
        "time": "7:05 PM EDT", "weather": "78°F | Wind 9 mph Out to RF", "grade": "BOOSTED +8% (B+)", "away": "Boston Red Sox", "home": "New York Yankees",
        "away_arsenal": {"Fastball": "40%", "Slider": "30%", "Changeup": "20%", "Curveball": "10%"},
        "home_arsenal": {"4-Seam Fastball": "46%", "Slider": "30%", "Sinker": "14%", "Changeup": "10%"}
    },
    "Los Angeles Dodgers @ San Francisco Giants": {
        "time": "10:10 PM EDT", "weather": "55°F | Wind 14 mph Out from Bay", "grade": "SUPPRESSED -15% (D-)", "away": "Los Angeles Dodgers", "home": "San Francisco Giants",
        "away_arsenal": {"4-Seam Fastball": "45%", "Slider": "30%", "Curveball": "15%", "Sinker": "10%"},
        "home_arsenal": {"Sinker": "38%", "Slider": "32%", "Changeup": "20%", "Curveball": "10%"}
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
away_team, home_team = current_game_info["away"], current_game_info["home"]

st.markdown("---")
st.markdown(f"""
<div class="card-box" style="border-color: #00ffcc;">
    <h3 style="margin: 0; color: #00ffcc;">⚡ Active Analysis: {st.session_state.selected_matchup}</h3>
    <p style="margin: 5px 0 0 0; color: #ccc;">🌤️ Weather Conditions: {current_game_info['weather']} &nbsp;|&nbsp; <b>Weather Grade: {current_game_info['grade']}</b></p>
</div>
""", unsafe_allow_html=True)

# COLOR-CODING STYLING FUNCTION FOR DATAFRAMES
def color_matchup_grade(val):
    """Color codes based on performance indicators embedded in strings"""
    if any(tag in str(val) for tag in ["🟢", "A+", "A", "B+", ".36", ".37", ".38", ".5"]):
        return 'background-color: #0d2818; color: #2ecc71; font-weight: 600;'
    elif any(tag in str(val) for tag in ["🔴", "D", "F", ".28", ".29", ".30", ".31"]):
        return 'background-color: #381313; color: #e74c3c; font-weight: 600;'
    return ''

# FULL TEAM LINEUP BOARDS WITH COLOR CODING
col_away_lineup, col_home_lineup = st.columns(2)

with col_away_lineup:
    st.markdown(f'<div class="section-title">🔴 {away_team} Lineup (vs. {home_team} Pitch Mix)</div>', unsafe_allow_html=True)
    away_lineup_data = [
        {"Bat": "1. C. Carrigg (CF)", "Matchup": "🟢 Elite (.385 wOBA)", "AVG": ".285", "SLG": ".480", "wOBA": ".362", "Hard%": "42.1%"},
        {"Bat": "2. J. Wood (LF)", "Matchup": "🟢 Elite (.410 wOBA)", "AVG": ".272", "SLG": ".510", "wOBA": ".375", "Hard%": "48.6%"},
        {"Bat": "3. C. Crews (RF)", "Matchup": "🟢 Good (.350 wOBA)", "AVG": ".265", "SLG": ".460", "wOBA": ".348", "Hard%": "40.2%"},
        {"Bat": "4. N. Schuelke (1B)", "Matchup": "🟡 Neutral (.320 wOBA)", "AVG": ".250", "SLG": ".440", "wOBA": ".332", "Hard%": "39.0%"},
        {"Bat": "5. L. Garcia (2B)", "Matchup": "🟡 Neutral (.315 wOBA)", "AVG": ".278", "SLG": ".410", "wOBA": ".325", "Hard%": "35.4%"},
        {"Bat": "6. I. Tena (3B)", "Matchup": "🔴 Poor (.285 wOBA)", "AVG": ".245", "SLG": ".390", "wOBA": ".305", "Hard%": "34.1%"},
        {"Bat": "7. CJ Abrams (SS)", "Matchup": "🟢 Good (.340 wOBA)", "AVG": ".260", "SLG": ".450", "wOBA": ".335", "Hard%": "41.0%"},
        {"Bat": "8. K. Ruiz (C)", "Matchup": "🔴 Poor (.270 wOBA)", "AVG": ".240", "SLG": ".370", "wOBA": ".285", "Hard%": "31.2%"},
        {"Bat": "9. T. Lipscomb (DH)", "Matchup": "🔴 Poor (.280 wOBA)", "AVG": ".235", "SLG": ".380", "wOBA": ".295", "Hard%": "33.5%"}
    ]
    df_away = pd.DataFrame(away_lineup_data)
    styled_away = df_away.style.applymap(color_matchup_grade, subset=['Matchup', 'wOBA'])
    st.dataframe(styled_away, use_container_width=True, hide_index=True)

with col_home_lineup:
    st.markdown(f'<div class="section-title">🔵 {home_team} Lineup (vs. {away_team} Pitch Mix)</div>', unsafe_allow_html=True)
    home_lineup_data = [
        {"Bat": "1. E. Tovar (SS)", "Matchup": "🟢 Good (.345 wOBA)", "AVG": ".275", "SLG": ".455", "wOBA": ".340", "Hard%": "43.2%"},
        {"Bat": "2. R. McMahon (3B)", "Matchup": "🟢 Elite (.390 wOBA)", "AVG": ".258", "SLG": ".470", "wOBA": ".352", "Hard%": "45.0%"},
        {"Bat": "3. B. Doyle (CF)", "Matchup": "🟢 Elite (.380 wOBA)", "AVG": ".268", "SLG": ".465", "wOBA": ".345", "Hard%": "46.2%"},
        {"Bat": "4. E. Montero (1B)", "Matchup": "🟡 Neutral (.315 wOBA)", "AVG": ".250", "SLG": ".430", "wOBA": ".320", "Hard%": "38.5%"},
        {"Bat": "5. H. Goodman (C)", "Matchup": "🟡 Neutral (.310 wOBA)", "AVG": ".242", "SLG": ".420", "wOBA": ".310", "Hard%": "40.1%"},
        {"Bat": "6. N. Jones (RF)", "Matchup": "🟢 Good (.335 wOBA)", "AVG": ".255", "SLG": ".410", "wOBA": ".325", "Hard%": "36.8%"},
        {"Bat": "7. S. Bouchard (LF)", "Matchup": "🔴 Poor (.295 wOBA)", "AVG": ".238", "SLG": ".390", "wOBA": ".308", "Hard%": "35.0%"},
        {"Bat": "8. A. Trejo (2B)", "Matchup": "🔴 Poor (.280 wOBA)", "AVG": ".245", "SLG": ".360", "wOBA": ".290", "Hard%": "30.4%"},
        {"Bat": "9. P. Severino (DH)", "Matchup": "🔴 Poor (.275 wOBA)", "AVG": ".230", "SLG": ".375", "wOBA": ".288", "Hard%": "32.0%"}
    ]
    df_home = pd.DataFrame(home_lineup_data)
    styled_home = df_home.style.applymap(color_matchup_grade, subset=['Matchup', 'wOBA'])
    st.dataframe(styled_home, use_container_width=True, hide_index=True)

st.markdown("---")

# PITCHER PITCH MIX VS BATTER HITTING PERFORMANCE
st.markdown('<div class="section-title">📊 Detailed Pitcher vs. Batter Arsenal Breakdown</div>', unsafe_allow_html=True)
col_sel1, col_sel2 = st.columns(2)
with col_sel1:
    all_batters = [row["Bat"] for row in away_lineup_data] + [row["Bat"] for row in home_lineup_data]
    selected_batter = st.selectbox("Select Batter for Deep Dive:", options=all_batters)

with col_sel2:
    is_away_batter = selected_batter in [row["Bat"] for row in away_lineup_data]
    opposing_pitcher_name = home_team + " Starter" if is_away_batter else away_team + " Starter"
    opposing_arsenal = current_game_info["home_arsenal"] if is_away_batter else current_game_info["away_arsenal"]
    
    st.markdown(f"""
    <div style="background-color: #161b22; padding: 8px 12px; border-radius: 8px; border: 1px solid #222632; margin-top: 24px;">
        <span style="color: #9ba1a6; font-size: 0.8rem;">Opposing Starting Pitcher:</span><br/>
        <b style="color: #00ffcc; font-size: 0.95rem;">{opposing_pitcher_name}</b>
    </div>
    """, unsafe_allow_html=True)

comparison_rows = []
for pitch, usage in opposing_arsenal.items():
    comparison_rows.append({
        "Pitch Type": pitch,
        "Pitcher Usage%": usage,
        "Batter BA": ".285" if "Fastball" in pitch else ".230",
        "Batter SLG": ".510" if "Fastball" in pitch else ".390",
        "Batter wOBA": ".370" if "Fastball" in pitch else ".305",
        "Whiff%": "18.5% (Good)" if "Fastball" in pitch else "34.0% (Vulnerable)"
    })

df_comparison = pd.DataFrame(comparison_rows)
st.markdown(f"<p style='color: #00ffcc; font-weight: 600; margin-top: 15px;'>Matchup Matrix: {selected_batter} vs. {opposing_pitcher_name} Arsenal</p>", unsafe_allow_html=True)
st.dataframe(df_comparison, use_container_width=True, hide_index=True)

st.markdown("---")

# STARTING PITCHER MATCHUP COMPARISON
st.markdown('<div class="section-title">🎯 Starting Pitcher Matchup Breakdown</div>', unsafe_allow_html=True)
p_cols = st.columns(2)
with p_cols[0]:
    away_mix_str = ", ".join([f"{k} ({v})" for k, v in current_game_info["away_arsenal"].items()])
    st.markdown(f"""
    <div class="card-box">
        <h4 style="color: #00ffcc; margin-top:0;">Away Starter ({away_team})</h4>
        <p style="color: #9ba1a6; font-size: 0.85rem; margin-bottom: 5px;">ERA: 3.84 | WHIP: 1.22 | K/9: 8.9 | FIP: 4.10</p>
        <p style="font-size: 0.85rem;"><b>Pitch Arsenal:</b> {away_mix_str}</p>
    </div>
    """, unsafe_allow_html=True)
with p_cols[1]:
    home_mix_str = ", ".join([f"{k} ({v})" for k, v in current_game_info["home_arsenal"].items()])
    st.markdown(f"""
    <div class="card-box">
        <h4 style="color: #00ffcc; margin-top:0;">Home Starter ({home_team})</h4>
        <p style="color: #9ba1a6; font-size: 0.85rem; margin-bottom: 5px;">ERA: 4.45 | WHIP: 1.34 | K/9: 8.2 | FIP: 4.35</p>
        <p style="font-size: 0.85rem;"><b>Pitch Arsenal:</b> {home_mix_str}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<p style='color: #555960; text-align: center; font-size: 0.8rem; margin-top: 30px;'>doinksports.com • SharpPLAY Analytics Terminal</p>", unsafe_allow_html=True)
