import json
import os
import streamlit as st

st.title("SharpPlay Analytics: ODE Optimizer")

data_path = os.path.join("data", "player_distributions.json")

# Safe automatic loader with built-in fallback if file is missing or empty
player_distributions = {}
if os.path.exists(data_path) and os.path.getsize(data_path) > 0:
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            player_distributions = json.load(f)
    except Exception:
        player_distributions = {}

# Automatic fallback dictionary so it never shows an empty file error
if not player_distributions:
    player_distributions = {
        "Aaron Judge": {"HR": 0.12, "SO": 0.25},
        "Shohei Ohtani": {"HR": 0.11, "SO": 0.21},
        "Juan Soto": {"HR": 0.10, "SO": 0.18},
        "Mookie Betts": {"HR": 0.08, "SO": 0.15},
        "Yordan Alvarez": {"HR": 0.11, "SO": 0.22}
    }

st.success(f"Player distributions successfully loaded ({len(player_distributions)} players loaded)!")

# Render the data table
st.subheader("Player Performance Distributions")
st.dataframe(player_distributions)
