import streamlit as st


# Validate topic and goal selection
if not st.session_state.get("topic") or not st.session_state.get("goal"):
    st.error("Please select a topic and goal first.")
    #Topic and gaol delete instead only one is set.
    for key in ["topic", "goal"]:
            if key in st.session_state:
                del st.session_state[key]
    if st.button("Select topic and goals"):
        st.switch_page("views/goals.py")
    st.stop()


# UI
st.subheader(f"{st.session_state["topic"]}: {st.session_state["goal"]}")
# Show video if available
if st.session_state["video_url"] == st.session_state["video_url"]:
     # is true when not nan
     st.video(st.session_state["video_url"])
else:
     st.warning("No video available")

# Button to rules
if st.button("Read the rules"):
    st.switch_page("views/rules.py")

# Button to assessment
if st.button("Go to the quiz"):
    st.switch_page("views/assessment.py")