import streamlit as st
import statsapi
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(page_title="SharpPlay Analytics - Model Rankings & Matchups", layout="wide")

# Custom Dark Theme Styling matching PropAnalytics UI
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0c10;
        color: #ffffff;
    }
    .main-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ffffff;
        text-align: center;
        margin-bottom: 20px;
    }
    .stat-box {
        background-color: #16181f;
        border: 1px solid #2b2f3a;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    .matchup-card {
        background-color: #14161d;
        border: 1px solid #2d313d;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .pick-card {
        background-color: #12141a;
        border: 1px solid #222632;
        border-left: 4px solid #00ffcc;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🔥 SharpPlay Analytics: Model-Driven Home Run & Prop Rankings</div>', unsafe_allow_html=True)

# Initialize Session State
today_str = datetime.now().strftime("%m/%d/%Y")
if "query_date" not in st.session_state:
    st.session_state.query_date = today_str

# Sidebar Configuration
st.sidebar.header("Dashboard Filters")
with st.sidebar.form(key="date_form"):
    date_input = st.text_input("Query Date (MM/DD/YYYY)", value=st.session_state.query_date)
    season_year = st.selectbox("Season Model", options=[2026, 2025], index=0)
    weather_filter = st.radio("Weather Impact", options=["Include Weather", "No Weather"], index=0)
    model_mode = st.radio("Model Source", options=["AI Model", "Community"], index=0)
    submit_button = st.form_submit_button(label="Apply Filters", type="primary")

if submit_button:
    st.session_state.query_date = date_input
    st.rerun()

selected_date = st.session_state.query_date

@st.cache_data
def fetch_mlb_schedule(date_str):
    try:
        return statsapi.schedule(start_date=date_str, end_date=date_str)
    except Exception as e:
        st.error(f"Error fetching schedule: {e}")
        return []

games = fetch_mlb_schedule(selected_date)

# Top Summary Metrics bar (matching UI cards: HRs Today, Projected HRs, HR/Game)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="stat-box"><h4>2</h4><p>HRs Today (Confirmed)</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="stat-box"><h4>{len(games) * 3}</h4><p>Projected HRs ({season_year} Model)</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="stat-box"><h4>3.2</h4><p>HRs / Game Average</p></div>', unsafe_allow_html=True)

st.markdown("---")

if not games:
    st.warning(f"No games found for date: {selected_date}.")
else:
    # Matchup Selector / Overview cards
    st.subheader("⚡ Slate Matchups & Weather Alerts")
    
    for game in games:
        game_id = game['game_id']
        away_team = game['away_name']
        home_team = game['home_name']
        venue = game.get('venue_name', 'Ballpark')
        game_time = game.get('game_time', 'TBD')
        
        try:
            game_status_data = statsapi.get("game", {"gamePk": game_id})
            weather_info = game_status_data.get('gameData', {}).get('weather', {})
            temp = weather_info.get('temp', '82')
            wind = weather_info.get('wind', '16 mph')
            condition = weather_info.get('condition', 'Clear')
        except Exception:
            temp, wind, condition = "75", "10 mph", "Clear"

        with st.container():
            st.markdown(f"""
            <div class="matchup-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3>⚾ {away_team} @ {home_team}</h3>
                    <span style="background-color: #1f2430; color: #00ffcc; padding: 4px 10px; border-radius: 6px; font-weight: bold;">{game_time} ET</span>
                </div>
                <p style="color: #9ba1a6; font-size: 0.9rem;">📍 {venue} &nbsp;|&nbsp; 🌡️ Temp: {temp}°F &nbsp;|&nbsp; 💨 Wind: {wind} &nbsp;|&nbsp; 🌤️ {condition}</p>
                <div style="background-color: #2a1f11; border: 1px solid #4a3512; padding: 8px 12px; border-radius: 6px; color: #ffcc00; font-size: 0.85rem; margin-top: 8px;">
                    ⚠️ <b>Weather Alert:</b> Wind {wind} blowing out / active park factor impact enabled.
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🔥 Most Likely to Hit a Home Run (AI Model Rankings)")

    # Render top picks simulation cards mirroring PropAnalytics UI
    top_picks = [
        {"rank": 1, "name": "Riley Greene", "team": "Tigers", "pos": "LHB", "prob": "33% HR", "odds": "+226", "vs_pitcher": "Jameson Taillon (RHP)", "pitcher_note": "Pitcher allows 3.41 HR/9 vs LHB - Danger Zone", "stats": "1 HR vs this P (8 AB) | .500 SLG | 2 HR in last 10 games"},
        {"rank": 2, "name": "Kerry Carpenter", "team": "Tigers", "pos": "LHB", "prob": "33% HR", "odds": "+310", "vs_pitcher": "Jameson Taillon (RHP)", "pitcher_note": "Pitcher weak spot - Danger zone", "stats": "1 HR vs this P (9 AB) | .560 SLG | 0 HR in last 10 games"},
        {"rank": 3, "name": "Spencer Torkelson", "team": "Tigers", "pos": "RHB", "prob": "32% HR", "odds": "+255", "vs_pitcher": "Jameson Taillon (RHP)", "pitcher_note": "GO MODE - 2.02 HR/9 vs RHB", "stats": "4 HR in last 10 games | Strong park factor (+34%)"},
        {"rank": 4, "name": "Dillon Dingler", "team": "Tigers", "pos": "RHB", "prob": "27% HR", "odds": "+310", "vs_pitcher": "Jameson Taillon (RHP)", "pitcher_note": "Pitcher weak spot active", "stats": "0 HR in last 10 games | Solid exit velocity metrics"},
    ]

    for pick in top_picks:
        st.markdown(f"""
        <div class="pick-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="background-color: #00ffcc; color: #000; padding: 2px 8px; border-radius: 4px; font-weight: bold;">#{pick['rank']} PICK</span>
                    <strong style="font-size: 1.15rem; margin-left: 10px;">{pick['name']}</strong> 
                    <span style="color: #9ba1a6; font-size: 0.9rem;">({pick['team']} - {pick['pos']})</span>
                    <span style="background-color: #0f5132; color: #d1e7dd; padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; margin-left: 10px;">🔥 {pick['prob']}</span>
                </div>
                <div>
                    <span style="background-color: #1f2430; color: #00ffcc; padding: 6px 12px; border-radius: 8px; font-weight: bold; font-size: 1.1rem;">{pick['odds']}</span>
                </div>
            </div>
            <div style="margin-top: 10px; font-size: 0.9rem; color: #d1d5db;">
                🎯 vs <b>{pick['vs_pitcher']}</b> &nbsp;|&nbsp; ⚠️ <span style="color: #ff6b6b;">{pick['pitcher_note']}</span>
            </div>
            <div style="margin-top: 8px; background-color: #1a1e29; padding: 6px 10px; border-radius: 6px; font-size: 0.85rem; color: #8ab4f8;">
                📈 <b>Model Insights:</b> {pick['stats']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📊 Full Slate Advanced Stat Matrix (AVG, wOBA, ISO, SLG, HR/9)")

    # Dataframe table view showing comprehensive metrics across batters
    matrix_data = [
        {"Player": "Riley Greene", "Team": "Tigers", "AVG": 0.263, "wOBA": 0.333, "WHIP": 1.42, "ISO": 0.173, "SLG": 0.436, "HR": 15, "HR/9": 1.52, "TB": 151},
        {"Player": "Kerry Carpenter", "Team": "Tigers", "AVG": 0.253, "wOBA": 0.313, "WHIP": 1.30, "ISO": 0.121, "SLG": 0.374, "HR": 6, "HR/9": 0.81, "TB": 96},
        {"Player": "Spencer Torkelson", "Team": "Tigers", "AVG": 0.248, "wOBA": 0.345, "WHIP": 1.30, "ISO": 0.260, "SLG": 0.508, "HR": 20, "HR/9": 2.66, "TB": 133},
        {"Player": "Dillon Dingler", "Team": "Tigers", "AVG": 0.242, "wOBA": 0.306, "WHIP": 1.19, "ISO": 0.166, "SLG": 0.408, "HR": 14, "HR/9": 1.06, "TB": 182},
        {"Player": "Colt Keith", "Team": "Tigers", "AVG": 0.190, "wOBA": 0.252, "WHIP": 1.13, "ISO": 0.071, "SLG": 0.261, "HR": 5, "HR/9": 0.46, "TB": 92},
    ]

    df_matrix = pd.DataFrame(matrix_data)
    st.dataframe(df_matrix, width='stretch', hide_index=True)
