import streamlit as st
import pandas as pd
from gemini_utils import generate_feedback
import random


# Validate topic and goal selection
if not st.session_state.get("topic") or not st.session_state.get("goal"):
    st.error("Please select a topic and goal first.")
    st.stop()

# Fetch selected goal and content
selected_topic = st.session_state["topic"]
selected_goal = st.session_state["goal"]
df_quizitems = st.session_state["df_quizitems"]
filtered_df = df_quizitems[(df_quizitems["topic"] == selected_topic) & (df_quizitems["goal"] == selected_goal)]
test_items = filtered_df.to_dict("records")

# Ensure there are at least 3 items to sample
if len(test_items) >= 3:
    selected_items = random.sample(test_items, 3)
else:
    selected_items = test_items  # If fewer than 3, take all available


# Initialize state
for key, default in {
    "question_index": 0,
    "show_feedback": False,
    "last_feedback": "",
    "last_correct": "",
    "last_question": "",
    "last_user_answer": "",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

current_index = st.session_state.question_index

# If assessment is ongoing
if current_index < len(selected_items):
    item = selected_items[current_index]
    st.subheader(f"{selected_goal}: Question {current_index + 1} of {len(selected_items)}")
    if "text" in item and pd.notna(item["text"]):
        st.write(item["text"])
    else:
        # kein Text, aber dann als leeres Feld
        item["text"] = ""
    user_answer = st.text_input(item["question"], key=f"input_{current_index}")

    if st.button("Submit Answer"):
        feedback = generate_feedback(
            text = item["text"],
            question=item["question"],
            correct_response=item["correct_answer"],
            student_response=user_answer
        )
        st.session_state.last_feedback = feedback
        st.session_state.last_correct = item["correct_answer"]
        st.session_state.last_text = item["text"]
        st.session_state.last_question = item["question"]
        st.session_state.last_user_answer = user_answer
        st.session_state.show_feedback = True

    if st.session_state.show_feedback:
        st.success(st.session_state.last_feedback)
        if st.button("Next Question"):
            st.session_state.question_index += 1
            st.session_state.show_feedback = False
            st.rerun()

# If all questions completed
else:
    st.success("🎉 Assessment complete! Well done.")
    if st.button("Restart"):
        for key in ["question_index", "show_feedback", "last_feedback", "last_correct", "last_question", "last_user_answer"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
