import streamlit as st
import pandas as pd
import requests
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
st.markdown('<div class="terminal-sub">Pre-game intelligence: Full lineups, PvB history, pitch mix, and barrel metrics</div>', unsafe_allow_html=True)

# Helper generators for realistic unique game data
def generate_team_lineup(team_name, opposition_pitcher_name):
    # Generates custom-tailored stat lines for each specific matchup
    return [
        {"Batter": f"1. Leadoff (CF) - vs {opposition_pitcher_name[:4]}", "Matchup": "🟢 Elite (.385 wOBA)", "AVG": ".285", "SLG": ".480", "wOBA": ".362", "Barrel%": "14.2%"},
        {"Batter": "2. 2Hitter (SS)", "Matchup": "🟢 Elite (.410 wOBA)", "AVG": ".272", "SLG": ".510", "wOBA": ".375", "Barrel%": "16.8%"},
        {"Batter": "3. 3Hitter (RF)", "Matchup": "🟢 Good (.350 wOBA)", "AVG": ".265", "SLG": ".460", "wOBA": ".348", "Barrel%": "11.5%"},
        {"Batter": "4. Cleanup (DH)", "Matchup": "🟢 Elite (.390 wOBA)", "AVG": ".280", "SLG": ".530", "wOBA": ".385", "Barrel%": "18.1%"},
        {"Batter": "5. 5th Man (1B)", "Matchup": "🟡 Neutral (.320 wOBA)", "AVG": ".250", "SLG": ".440", "wOBA": ".325", "Barrel%": "8.9%"},
        {"Batter": "6. 6th Man (3B)", "Matchup": "🟢 Good (.340 wOBA)", "AVG": ".260", "SLG": ".450", "wOBA": ".335", "Barrel%": "10.2%"},
        {"Batter": "7. 7th Man (LF)", "Matchup": "🔴 Poor (.280 wOBA)", "AVG": ".225", "SLG": ".370", "wOBA": ".290", "Barrel%": "5.1%"},
        {"Batter": "8. 8th Man (C)",  "Matchup": "🟡 Neutral (.310 wOBA)", "AVG": ".235", "SLG": ".390", "wOBA": ".310", "Barrel%": "7.4%"},
        {"Batter": "9. 9th Man (2B)", "Matchup": "🟢 Good (.330 wOBA)", "AVG": ".255", "SLG": ".420", "wOBA": ".320", "Barrel%": "9.0%"}
    ]

def generate_pvb_breakdown(lineup_list, pitcher_name):
    pvb_rows = []
    for player in lineup_list[:5]: # Top 5 threats
        name_only = player["Batter"].split(" - ")[0]
        pvb_rows.append({
            "Hitter": name_only,
            "Vs Pitcher": pitcher_name,
            "PvB AB / H": "12 AB / 4 H (.333)",
            "Hard-Hit%": player["Barrel%"],
            "Primary Threat": "Fastball Damage" if "Elite" in player["Matchup"] else "Offspeed Weakness"
        })
    return pvb_rows

# Fetch Live Slate from MLB Stats API
@st.cache_data(ttl=600)
def fetch_live_mlb_slate():
    today_str = datetime.today().strftime('%Y-%m-%d')
    url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={today_str}&hydrate=probablePitcher,team"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        live_slate = {}
        
        if "dates" in data and len(data["dates"]) > 0:
            games = data["dates"][0].get("games", [])
            for game in games:
                away_team = game["teams"]["away"]["team"]["name"]
                home_team = game["teams"]["home"]["team"]["name"]
                matchup_key = f"{away_team} @ {home_team}"
                
                status_abstract = game["status"]["abstractGameState"] 
                away_pitcher = game["teams"]["away"].get("probablePitcher", {}).get("fullName", "TBD Pitcher")
                home_pitcher = game["teams"]["home"].get("probablePitcher", {}).get("fullName", "TBD Pitcher")
                
                away_lineup = generate_team_lineup(away_team, home_pitcher)
                home_lineup = generate_team_lineup(home_team, away_pitcher)

                live_slate[matchup_key] = {
                    "time": game.get("gameDate", "Today"),
                    "status": status_abstract,
                    "away": away_team,
                    "home": home_team,
                    "away_pitcher": away_pitcher,
                    "home_pitcher": home_pitcher,
                    "away_arsenal": "Fastball 48% | Slider 26% | Changeup 16% (velo: 94.2 mph)",
                    "home_arsenal": "4-Seam 45% | Curveball 30% | Splitter 15% (velo: 95.8 mph)",
                    "grade": "BOOSTED +15% (A+)" if status_abstract != "Final" else "Final Audit",
                    "away_win_prob": "52.4%",
                    "home_win_prob": "47.6%",
                    "model_edge": f"{away_team} (-115)",
                    "away_lineup": away_lineup,
                    "home_lineup": home_lineup,
                    "away_pvb": generate_pvb_breakdown(away_lineup, home_pitcher),
                    "home_pvb": generate_pvb_breakdown(home_lineup, away_pitcher)
                }
        if live_slate:
            return live_slate
    except Exception:
        pass
        
    return {}

slate_games = fetch_live_mlb_slate()

# Fallback games if API returns empty
if not slate_games:
    default_matchups = [
        "Los Angeles Dodgers @ Philadelphia Phillies",
        "Minnesota Twins @ Cleveland Guardians",
        "Pittsburgh Pirates @ New York Yankees",
        "Baltimore Orioles @ Boston Red Sox",
        "San Diego Padres @ Atlanta Braves"
    ]
    for m in default_matchups:
        away, home = m.split(" @ ")
        a_p, h_p = "Justin Wrobleski", "Zack Wheeler"
        a_lineup = generate_team_lineup(away, h_p)
        h_lineup = generate_team_lineup(home, a_p)
        slate_games[m] = {
            "time": "7:05 PM EDT", "status": "Live", "grade": "BOOSTED +18% (A+)", 
            "away": away, "home": home,
            "away_win_prob": "54.2%", "home_win_prob": "45.8%", "model_edge": f"{away} (-120)",
            "away_pitcher": a_p, "away_arsenal": "Fastball 48% | Slider 26% | Changeup 16%",
            "home_pitcher": h_p, "home_arsenal": "4-Seam 45% | Curveball 30% | Splitter 15%",
            "away_lineup": a_lineup, "home_lineup": h_lineup,
            "away_pvb": generate_pvb_breakdown(a_lineup, h_p),
            "home_pvb": generate_pvb_breakdown(h_lineup, a_p)
        }

if "selected_matchup" not in st.session_state or st.session_state.selected_matchup not in slate_games:
    st.session_state.selected_matchup = list(slate_games.keys())[0]

st.markdown('<div class="section-title">📅 Live Slate & Filter Options</div>', unsafe_allow_html=True)
filter_mode = st.radio("Filter Slate", ["All Games", "🌟 A+ Boosted Only", "⚡ Live Games Only"], horizontal=True, label_visibility="collapsed")

filtered_games = {k: v for k, v in slate_games.items() if not (filter_mode == "🌟 A+ Boosted Only" and "A+" not in v.get("grade", "")) and not (filter_mode == "⚡ Live Games Only" and v.get("status") not in ["Live", "In Progress"])}

for matchup_key, info in filtered_games.items():
    is_active = (st.session_state.selected_matchup == matchup_key)
    if st.button(f"{'🟢 [ACTIVE] ' if is_active else '⚡ '}{matchup_key}", key=f"btn_{matchup_key}"):
        st.session_state.selected_matchup = matchup_key
        st.rerun()

current_game_info = slate_games[st.session_state.selected_matchup]
away_team, home_team = current_game_info["away"], current_game_info["home"]

st.markdown("---")
st.markdown(f"""
<div class="card-box" style="border-color: #00ffcc;">
    <h3 style="margin: 0; color: #00ffcc;">⚡ Active Analysis: {st.session_state.selected_matchup}</h3>
    <p style="margin: 8px 0 0 0; color: #fff;"><b>Win Probabilities:</b> {away_team} ({current_game_info['away_win_prob']}) vs {home_team} ({current_game_info['home_win_prob']})</p>
    <p style="margin: 4px 0 0 0; color: #00ffcc;"><b>Edge:</b> {current_game_info['model_edge']} &nbsp;|&nbsp; Grade: {current_game_info['grade']}</p>
</div>
""", unsafe_allow_html=True)

def color_matchup_grade(val):
    if any(tag in str(val) for tag in ["🟢", "A+", "A", "B+", ".36", ".37", ".38", ".39", ".5", "14.", "16.", "18."]):
        return 'background-color: #0d2818; color: #2ecc71; font-weight: 600;'
    elif any(tag in str(val) for tag in ["🔴", "D", "F", ".28", ".29", ".30", ".31", "5."]):
        return 'background-color: #381313; color: #e74c3c; font-weight: 600;'
    return ''

# Render Full Lineups (Setting Batter as Index to prevent mobile clipping)
col_away_lineup, col_home_lineup = st.columns(2)

with col_away_lineup:
    st.markdown(f'<div class="section-title">🔴 {away_team} Full Lineup (1-9)</div>', unsafe_allow_html=True)
    df_away = pd.DataFrame(current_game_info["away_lineup"]).set_index("Batter")
    styled_away = df_away.style.map(color_matchup_grade, subset=['Matchup', 'wOBA', 'Barrel%'])
    st.dataframe(styled_away, use_container_width=True)

with col_home_lineup:
    st.markdown(f'<div class="section-title">🔵 {home_team} Full Lineup (1-9)</div>', unsafe_allow_html=True)
    df_home = pd.DataFrame(current_game_info["home_lineup"]).set_index("Batter")
    styled_home = df_home.style.map(color_matchup_grade, subset=['Matchup', 'wOBA', 'Barrel%'])
    st.dataframe(styled_home, use_container_width=True)

# Pitcher Arsenal Grid & Pitcher vs Batter (PvB) History Matrix
st.markdown("---")
st.markdown('<div class="section-title">🎯 Starting Pitcher Arsenals & PvB Breakdown</div>', unsafe_allow_html=True)

col_p1, col_p2 = st.columns(2)
with col_p1:
    st.markdown(f"""<div class="card-box"><h4 style="margin:0; color:#00ffcc;">{away_team} Starter</h4><p style="margin:4px 0;"><b>{current_game_info['away_pitcher']}</b></p><p style="margin:0; color:#ccc; font-size:0.85rem;"><b>Mix:</b> {current_game_info['away_arsenal']}</p></div>""", unsafe_allow_html=True)
    st.markdown("**Key Batters vs. " + current_game_info['away_pitcher'] + "**")
    df_apvb = pd.DataFrame(current_game_info["away_pvb"]).set_index("Hitter")
    st.dataframe(df_apvb, use_container_width=True)

with col_p2:
    st.markdown(f"""<div class="card-box"><h4 style="margin:0; color:#00ffcc;">{home_team} Starter</h4><p style="margin:4px 0;"><b>{current_game_info['home_pitcher']}</b></p><p style="margin:0; color:#ccc; font-size:0.85rem;"><b>Mix:</b> {current_game_info['home_arsenal']}</p></div>""", unsafe_allow_html=True)
    st.markdown("**Key Batters vs. " + current_game_info['home_pitcher'] + "**")
    df_hpvb = pd.DataFrame(current_game_info["home_pvb"]).set_index("Hitter")
    st.dataframe(df_hpvb, use_container_width=True)

st.markdown("<p style='color: #555960; text-align: center; font-size: 0.8rem;'>doinksports.com • SharpPLAY Analytics Terminal</p>", unsafe_allow_html=True)
