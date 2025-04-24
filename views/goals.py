import streamlit as st

# -- Init session state ---
for key, default in {
    "subject": None,
    "learning_goal": None,
    "hobby": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# --- Subject selection ---
col1, col2 = st.columns([1, 8])
with col1:
    st.image("images/masteryx.jpg", width=60)
with col2:
    st.title("Welcome To MasteryX")

st.subheader("Set your learning goal!", divider="blue")

subject_options = ["English", "Math", "Biology"]
st.session_state["subject"] = st.selectbox("Choose your subject:", [""] + subject_options)

# --- Learning goals per subject ---
learning_goals = {
    "English": ["Present Simple", "Present Continuous", "Past Simple", "Present Perfect"],
    "Math": ["Linear Equations", "Fractions", "Word Problems", "Geometry Basics"],
    "Biology": ["Photosynthesis", "Human Organs", "Cells and DNA", "Ecosystems"]
}

if st.session_state["subject"]:
    st.session_state["learning_goal"] = st.selectbox(
        "Select a learning goal:",
        [""] + learning_goals[st.session_state["subject"]]
    )

# --- Hobby or topic of interest ---
if st.session_state["subject"] and st.session_state["learning_goal"]:
    hobby = ["Music", "Basketball", "Fashion", "Soccer", "Painting", "Dancing", "Cooking", "Racing Cars", "Gaming"]
    st.session_state["hobby"] = st.pills("Choose a topic of interest:", hobby, selection_mode="single")

# --- Confirmation summary ---
if st.session_state["learning_goal"] and st.session_state["extra"] and st.session_state["hobby"] :
    st.switch_page("views/assessment.py")
else:
    st.info("Please make all your selections to proceed.")

