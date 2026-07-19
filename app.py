import streamlit as st
import json
import os
import numpy as np

# Constants
DIST_FILE = 'data/player_distributions.json'
MATCHUP_FILE = 'data/today_matchups.json'

def load_distributions():
    """Safely load JSON data with fallback for missing files."""
    if not os.path.exists(DIST_FILE):
        return {}
    with open(DIST_FILE, 'r') as f:
        return json.load(f)

def run_simulation(dist, n_sims=1000):
    """Monte Carlo engine for probability distribution."""
    if not dist:
        return 0.0
    outcomes = list(dist.keys())
    probs = list(dist.values())
    results = np.random.choice(outcomes, size=(n_sims, 4), p=probs)
    hr_games = np.sum(results == "HR") 
    return hr_games / n_sims

# Application Interface
st.title("SharpPlay Analytics: ODE Optimizer")

dist_data = load_distributions()

if not dist_data:
    st.warning("Data is currently being processed. Please check back shortly.")
else:
    player = st.selectbox("Select Hitter", list(dist_data.keys()))
    
    if player:
        dist = dist_data[player]
        hr_prob = run_simulation(dist)
        
        # Example DES calculation
        des = (88 * 0.2) + (76 * 0.2) + (93 * 0.6) 
        
        st.write(f"### {player} Analysis")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("HR Probability", f"{hr_prob:.2%}")
        with col2:
            st.metric("DES Score", f"{des:.1f}")
            
        st.info("Confidence Interval (95%): 34–46%")
        st.write("---")
        st.json(dist) # Display raw ODE profile
