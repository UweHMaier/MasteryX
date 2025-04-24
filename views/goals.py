import streamlit as st

# --- Dummy data structure (to be replaced by DB later) ---
learning_context = {
    "Tenses (English)": {
        "goals": ["Present Simple", "Present Continuous", "Past Simple", "Present Perfect"],
        "extras": ["Dancing", "Music", "Soccer", "Racing Cars"]
    },
    "Active and Passive Voice (English)": {
        "goals": ["Role of Subject", "Role of the Verb", "Role of the Object"],
        "extras": ["Dancing", "Music", "Soccer", "Racing Cars"]
    },
    "Adjectives (English)": {
        "goals": ["Negative Prefixes", "Comparative and Superlative Forms"],
        "extras": ["Dancing", "Music", "Soccer", "Racing Cars"]
    },
    "Trennbare und untrennbare Präfixe (German language)": {
        "goals": ["Trennbare Präfixe", "Untrennbare Präfixe", "Relativ trennbare Präfixe"],
        "extras": ["Dancing", "Music", "Soccer", "Racing Cars"]
    },
    "Stock Market (Economy)": {
        "goals": ["Basic Concepts", "Market Behavior", "Investment Strategies"],
        "extras": ["Tech Stocks", "Compound Interest"]
    },
    "Chinese Language": {
        "goals": ["Chinese Words", "Chinese Characters", "Chinese Idioms"],
        "extras": []
    },
    "Word Problems (Math)": {
        "goals": ["Addition", "Multiplication", "Subtraction", "Division"],
        "extras": ["Dancing", "Music", "Soccer", "Racing Cars"]
    },
    "Slavery (History education)": {
        "goals": ["Concept of Slavery", "Timeline of Slavery", "Impact of Slavery", "Slavery in today Society"],
        "extras": []
    }
}

# -- Init session state ---
for key, default in {
    "topic": None,
    "goal": None,
    "extra": None,
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
st.session_state.topic = st.selectbox("Choose your topic:", [""] + list(learning_context.keys()))

if st.session_state.topic:
    st.session_state.goal = st.selectbox("Select a learning goal:", [""] + learning_context[st.session_state.topic]["goals"])

    extras = learning_context[st.session_state.topic]["extras"]

    # If extras are available for this topic
    if st.session_state.goal and extras:
        st.session_state.extra = st.selectbox("Choose your interest:", [""] + extras)

        if st.session_state.extra:
            st.success(f"You're ready! ✅\n\nTopic: **{st.session_state.topic}**\nGoal: **{st.session_state.goal}**\nExtra: **{st.session_state.extra}**")
            st.switch_page("views/assessment.py")
    
    # If no extras — skip that part
    elif st.session_state.goal and not extras:
        st.session_state.extra = ""
        st.success(f"You're ready! ✅\n\nTopic: **{st.session_state.topic}**\nGoal: **{st.session_state.goal}**")
        st.switch_page("views/assessment.py")
