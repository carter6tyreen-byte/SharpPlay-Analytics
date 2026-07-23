import streamlit as st
import pandas as pd
import requests

# Page Configuration
st.set_page_config(
    page_title="SharpPlay Analytics",
    page_icon="⚾",
    layout="wide"
)

# App Header
st.title("⚾ SharpPlay Analytics Dashboard")
st.markdown("Live Major League Baseball statistics, data pipelines, and matchup insights.")

# Sidebar Controls
st.sidebar.header("Navigation & Filters")
view_mode = st.sidebar.selectbox(
    "Select Dashboard View",
    ["Live Matchups", "Odds Matrix", "System Status"]
)

# Main Content Area
if view_mode == "Live Matchups":
    st.subheader("Today's MLB Matchup Analytics")
    st.info("Fetching latest data feeds and building match projections...")
    
    # Placeholder layout for your data tables/matrix
    try:
        # Example container for your data integration
        # Replace or expand this with your actual API calls or json loading logic
        st.write("Matchup data feed is connected.")
        
        # Sample placeholder dataframe view
        sample_data = pd.DataFrame({
            "Game": ["NYY vs BOS", "LAD vs SF", "ATL vs NYM"],
            "Time (ET)" : ["7:05 PM", "10:10 PM", "7:20 PM"],
            "Status": ["Scheduled", "Scheduled", "Scheduled"]
        })
        st.table(sample_data)
        
    except Exception as e:
        st.error(f"Error loading live sports data: {e}")

elif view_mode == "Odds Matrix":
    st.subheader("Odds Matrix & Projections")
    st.write("Viewing current odds matrix configurations.")

else:
    st.subheader("System Status")
    st.success("Streamlit environment running on Python 3.11 successfully.")
    st.write("GitHub Actions pipeline and automated workflows are active.")
