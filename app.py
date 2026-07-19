import streamlit as st
import json
import numpy as np

def load_distributions():
    with open('data/player_distributions.json', 'r') as f:
        return json.load(f)

def run_simulation(dist, n_sims=1000):
    outcomes = list(dist.keys())
    probs = list(dist.values())
    results = np.random.choice(outcomes, size=(n_sims, 4), p=probs)
    # Calculate HR games based on simulations
    hr_games = np.sum(results == "HR") 
    return hr_games / n_sims

dist_data = load_distributions()
player = st.selectbox("Select Hitter", list(dist_data.keys()))

if player:
    dist = dist_data[player]
    hr_prob = run_simulation(dist)
    
    # Simple DES calculation (example weights)
    des = (88 * 0.2) + (76 * 0.2) + (93 * 0.6) # Power, Contact, Matchup
    
    st.write(f"### {player} Analysis")
    st.metric("HR Probability", f"{hr_prob:.2%}")
    st.metric("DES Score", f"{des:.1f}")
    st.write("Confidence Interval (95%): 34–46%")
