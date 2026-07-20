    with tab_overview:
        st.subheader("Color-Coded Matchup Grades")
        overview_data = pd.DataFrame({
            "Metric": ["Overall Matchup Grade", "Power Index (ISO)", "Contact Rate", "Chase Rate", "ODE Optimization Score"],
            f"Away Team ({selected_game['away']})": ["B+", "74", "78%", "24%", "82.4"],
            f"Home Team ({selected_game['home']})": ["A-", "81", "82%", "21%", "88.1"]
        })
        st.dataframe(overview_data) # Removed width=None
        
    with tab_pitcher_batter:
        st.subheader("Pitcher vs Batter Comparative Board")
        col_p, col_b = st.columns(2)
        with col_p:
            st.markdown("#### Starting Pitcher Profile")
            st.info(f"**Starting Pitcher for {selected_game['home']} / {selected_game['away']}**\n* ERA: 3.12\n* WHIP: 1.05\n* K/9: 10.4\n* Hard-Hit %: 31.2%")
        with col_b:
            st.markdown("#### Lineup Key Hitters")
            st.success("Core Metrics:\n* wOBA vs RHP: .350\n* Barrel %: 14.2%\n* Exit Velocity: 91.5 mph")
            
    with tab_pitch_mix:
        st.subheader("Pitch Mix & Usage Analytics")
        pitch_mix_df = pd.DataFrame({
            "Pitch Type": ["Fastball (4SFB)", "Slider", "Changeup", "Curveball"],
            "Usage %": ["45%", "28%", "17%", "10%"],
            "Whiff %": ["25%", "38%", "33%", "30%"],
            "Run Value": ["+2.1", "+4.5", "+1.2", "+0.8"]
        })
        st.dataframe(pitch_mix_df) # Removed width=None
