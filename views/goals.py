import streamlit as st
from PIL import Image
import requests
import streamlit as st

# iamge ID
#file_id = "1Q9XgaKTWu06D2O92WumkTr_tTlu8pLK-"  # replace with your real ID

# URL
#url = f"https://drive.google.com/uc?export=view&id={file_id}"

#response = requests.get(url)
#st.image(response.content)




# --- Detect first entry to this page and reset ---
if "first_visit_to_selection" not in st.session_state:
    for key in [
        "topic", "goal", "question_index", "show_feedback",
        "last_feedback", "last_correct", "last_question",
        "last_user_answer", "selected_items"
    ]:
        st.session_state.pop(key, None)
    st.session_state["first_visit_to_selection"] = True

# --- Layout ---
col1, col2 = st.columns([1, 8])
with col1:
    st.image("images/masteryx.jpg", width=60)
with col2:
    st.title("Welcome To MasteryX")

st.subheader("Set your learning goal!", divider="blue")

# Dynamische Statusanzeige mit Topic und Goal
if "topic" in st.session_state and st.session_state["topic"]:
    message = f"✅ Topic: {st.session_state['topic']}"
    if "goal" in st.session_state and st.session_state["goal"]:
        message += f"\n✅ Goal: {st.session_state['goal']}"
    st.success(message)

# --- Topic selection ---
df_rules = st.session_state["df_rules"]
topics = df_rules["topic"].dropna().unique().tolist()

# Wenn noch kein Thema gewählt wurde → Pillen anzeigen
if "topic" not in st.session_state or not st.session_state["topic"]:
    selected_topic = st.pills("Select your topic", options=topics, selection_mode="single")
    if selected_topic:
        st.session_state["topic"] = selected_topic
        st.rerun()  # Seite neu laden, um Thema anzuzeigen
else:
    selected_topic = st.session_state["topic"]


# --- Goal selection ---
if selected_topic:
    goals = (df_rules[df_rules["topic"] == selected_topic]["goal"].dropna().unique().tolist())

    # Nur anzeigen, wenn noch kein Ziel gewählt
    if "goal" not in st.session_state or not st.session_state["goal"]:
        selected_goal = st.pills("Select goal", options=goals, selection_mode="single")
        if selected_goal:
            st.session_state["goal"] = selected_goal
            st.rerun()
    else:
        if st.button("Read the Rules!"):
            st.session_state.pop("first_visit_to_selection", None)  # ✅ clear reset flag
            st.switch_page("views/rules.py")

