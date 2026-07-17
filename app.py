    # 4. Display Logic (DEBUG VERSION)
    if st.session_state.analysis_results is not None:
        st.write("---")
        st.write(f"### Results for {st.session_state.current_player}")
        
        # Debugging the data type and content
        st.write(f"**Data Type:** {type(st.session_state.analysis_results)}")
        
        # Check if it's a pandas DataFrame and if it's empty
        if hasattr(st.session_state.analysis_results, 'empty'):
            st.write(f"**Is DataFrame empty:** {st.session_state.analysis_results.empty}")
            if not st.session_state.analysis_results.empty:
                st.dataframe(st.session_state.analysis_results, use_container_width=True)
            else:
                st.warning("The engine returned an empty DataFrame.")
        else:
            st.write("**Raw Output:**", st.session_state.analysis_results)
    else:
        st.info("Select a player above to run the simulation.")
        
        # Debugging the data type and content
        st.write(f"**Data Type:** {type(st.session_state.analysis_results)}")
        
        # Check if it's a pandas DataFrame and if it's empty
        if hasattr(st.session_state.analysis_results, 'empty'):
            st.write(f"**Is DataFrame empty:** {st.session_state.analysis_results.empty}")
            if not st.session_state.analysis_results.empty:
                st.dataframe(st.session_state.analysis_results, use_container_width=True)
            else:
                st.warning("The engine returned an empty DataFrame.")
        else:
            st.write("**Raw Output:**", st.session_state.analysis_results)
    else:
        st.info("Select a player above to run the simulation.")

        
        # Debugging the data type and content
        st.write(f"**Data Type:** {type(st.session_state.analysis_results)}")
        
        # Check if it's a pandas DataFrame and if it's empty
        if hasattr(st.session_state.analysis_results, 'empty'):
            st.write(f"**Is DataFrame empty:** {st.session_state.analysis_results.empty}")
            if not st.session_state.analysis_results.empty:
                st.dataframe(st.session_state.analysis_results, use_container_width=True)
            else:
                st.warning("The engine returned an empty DataFrame.")
        else:
            st.write("**Raw Output:**", st.session_state.analysis_results)
    else:
        st.info("Select a player above to run the simulation.")
