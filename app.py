# --- Pitcher Section ---
st.subheader("Pitcher ERA Leaders")
pitcher_df = engine.get_pitcher_data()
if pitcher_df is not None and not pitcher_df.empty:
    # UPDATED: Use .map instead of .applymap
    styled_pitcher = pitcher_df.style.map(style_pitcher_era, subset=['Value'])
    st.dataframe(styled_pitcher, use_container_width=True)
else:
    st.warning("No pitcher data available.")

# --- Batter Section ---
st.subheader("Batter Home Run Leaders")
batter_df = engine.get_batter_data()
if batter_df is not None and not batter_df.empty:
    # UPDATED: Use .map instead of .applymap
    styled_batter = batter_df.style.map(style_batter_hr, subset=['Value'])
    st.dataframe(styled_batter, use_container_width=True)
else:
    st.warning("No batter data available.")
