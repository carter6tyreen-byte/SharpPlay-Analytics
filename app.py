# Create a cleaner display for the status
def color_status(val):
    color = 'green' if val == 'Final' else 'orange' if val == 'Scheduled' else 'blue'
    return f'color: {color}'

# Display in Streamlit
st.write("### ⚾ Today's SharpPLAY Matchups")
# This creates a more readable table for users
st.dataframe(df, use_container_width=True, hide_index=True)

# Add a section for potential "Sharp" insights
st.divider()
st.subheader("💡 Today's Insights")
st.info("No game analysis available yet—check back closer to first pitch!")
