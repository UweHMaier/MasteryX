import streamlit as st
from content import content

# Validate topic and goal selection
if not st.session_state.get("topic") or not st.session_state.get("goal"):
    st.error("Please select a topic and goal first.")
    st.stop()

# Fetch selected goal
selected_topic = st.session_state["topic"]
selected_goal_name = st.session_state["goal"]
goal_data = next(goal for goal in content[selected_topic]["goals"] if goal["name"] == selected_goal_name)
test_items = goal_data["test_items"]

# UI
st.title(f"Topic: {selected_topic}")
st.write(f"Learning goal: {selected_goal_name}")
st.markdown(f"**Rule:** {goal_data['rule']}")

# Button to assessment
if st.button("Go to the quiz"):
    st.switch_page("views/assessment.py")