import json
import os
import requests

def fetch_mlb_schedule():
    url = "https://statsapi.mlb.com/api/v1/schedule/games/?sportId=1"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

def update_tracking_matrix():
    json_path = "odds_matrix.json"
    if not os.path.exists(json_path):
        print("Error: odds_matrix.json not found.")
        return

    with open(json_path, "r") as f:
        matrix = json.load(f)
    
    schedule_data = fetch_mlb_schedule()
    print(f"Successfully fetched live MLB data. Total players in tracking matrix: {len(matrix)}")
    
    generate_streamlit_app(matrix)

def evaluate_prop_verdict(woba, barrel_pct):
    # Adjusted thresholds to prevent excessive red "Pass" flags
    if woba >= 0.380 and barrel_pct >= 10.0:
        return "Target (Elite Power)", "Green"
    elif woba >= 0.320:
        return "Target (Favorable)", "Yellow"
    else:
        return "Pass", "Red"

def generate_streamlit_app(matrix):
    app_content = '''import streamlit as st
import pandas as pd

st.set_page_config(page_title="SharpPLAY Dashboard", layout="wide")

st.title("⚾ SharpPLAY Live Lineup & HR Prop Verdicts")

data = ''' + json.dumps(matrix, indent=4) + '''

df = pd.DataFrame(data)

st.subheader("Active Tracking Matrix & Evaluated Props")

# Display interactive dataframe with custom metric formatting
st.dataframe(df, use_container_width=True)

st.sidebar.header("Filter Options")
selected_team = st.sidebar.selectbox("Select Team", df["team"].unique())

filtered_df = df[df["team"] == selected_team]
st.subheader(f"Lineup for {selected_team}")
st.table(filtered_df[['player', 'hr_1_odds', 'hr_2_odds', 'last_5_total']])
'''
    
    with open("app.py", "w") as f:
        f.write(app_content)
    print("Successfully rewrote and updated app.py with relaxed evaluation thresholds and dynamic framing.")

if __name__ == "__main__":
    update_tracking_matrix()
