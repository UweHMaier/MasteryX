import streamlit as st
from content import content

# -- Init session state ---
for key, default in {
    "topic": None,
    "goal": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- Layout ---
col1, col2 = st.columns([1, 8])
with col1:
    st.image("images/masteryx.jpg", width=60)
with col2:
    st.title("Welcome To MasteryX")

st.subheader("Set your learning goal!", divider="blue")

# --- Topic selection ---
st.session_state.topic = st.selectbox("Choose your topic:", [""] + list(content.keys()))

if st.session_state.topic:
    goals_list = content[st.session_state.topic]["goals"]
    goal_names = [goal["name"] for goal in goals_list]
    st.session_state.goal = st.selectbox("Select a learning goal:", [""] + goal_names)

    if st.session_state.goal:
        st.success(f"You're ready! ✅\n\nTopic: **{st.session_state.topic}**\nGoal: **{st.session_state.goal}**")
        st.switch_page("views/rules.py")
