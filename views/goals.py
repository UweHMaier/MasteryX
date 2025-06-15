import streamlit as st

# Delete state for quiz if user skips quiz and chooses new goal
for key in [
    "topic",
    "goal",
    "question_index",
    "show_feedback",
    "last_feedback",
    "last_correct",
    "last_question",
    "last_user_answer",
    "selected_items",
]:
    if key in st.session_state:
        del st.session_state[key]



# --- Layout ---
col1, col2 = st.columns([1, 8])
with col1:
    st.image("images/masteryx.jpg", width=60)
with col2:
    st.title("Welcome To MasteryX")

st.subheader("Set your learning goal!", divider="blue")

# --- Topic selection ---
df_quizitems = st.session_state["df_quizitems"]
topics = df_quizitems["topic"].dropna().unique().tolist()

# Detect topic change and reset goal
current_topic = st.session_state.get("topic", "")
selected_topic = st.pills("Topic", options=topics, selection_mode="single")
# If topic changed, reset goal
if selected_topic != current_topic:
    st.session_state["goal"] = None
st.session_state["topic"] = selected_topic

# --- Learning goal selection ---
if selected_topic:
    goals = (
        df_quizitems[df_quizitems["topic"] == selected_topic]["goal"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_goal = st.selectbox("Choose a learning goal:", [""] + goals)

    if selected_goal:
        st.session_state["goal"] = selected_goal
        st.success(
            f"You're ready! ✅\n\nTopic: **{st.session_state.topic}**\nGoal: **{st.session_state.goal}**"
        )
        st.switch_page("views/rules.py")
