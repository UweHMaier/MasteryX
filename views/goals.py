import streamlit as st

# --- Safety Check ---
if "content" not in st.session_state:
    st.error("Content not found. Please restart the app.")
    st.stop()

# --- Layout ---
col1, col2 = st.columns([1, 8])
with col1:
    st.image("images/masteryx.jpg", width=60)
with col2:
    st.title("Welcome To MasteryX")

st.subheader("Set your learning goal!", divider="blue")

# --- Topic selection ---
df = st.session_state["content"]
topics = df["topic"].dropna().unique().tolist()

# Detect topic change and reset goal
current_topic = st.session_state.get("topic", "")
selected_topic = st.selectbox(
    "Choose a topic:",
    [""] + topics,
    index=(topics.index(current_topic) + 1) if current_topic in topics else 0
)

# If topic changed, reset goal
if selected_topic != current_topic:
    st.session_state["goal"] = None

st.session_state["topic"] = selected_topic

# --- Learning goal selection ---
if selected_topic:
    goals = (
        df[df["topic"] == selected_topic]["goal"]
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
