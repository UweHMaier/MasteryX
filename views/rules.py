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
# Show image if available
if st.session_state["rule_image"] == st.session_state["rule_image"]:
     # is true when not nan
     st.image(st.session_state["rule_image"], width=500)

if st.session_state["rule_text"] == st.session_state["rule_text"]:
     # is true when not nan
     st.info(f"{st.session_state["rule_text"]}")
else:
     st.warning("No rules available.")


# Button to video if available
if st.session_state["video_url"] == st.session_state["video_url"]:
    if st.button("Go to the video"):
        st.switch_page("views/video.py")


# Button to assessment
if st.button("Go to the quiz"):
    st.switch_page("views/assessment.py")