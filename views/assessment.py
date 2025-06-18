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


# Random sampling of 3 items
if "selected_items" not in st.session_state:
    # Sample only once and store in session_state
    if len(test_items) >= 3:
        st.session_state.selected_items = random.sample(test_items, 3)
    else:
        st.session_state.selected_items = test_items

selected_items = st.session_state.selected_items
current_index = st.session_state.question_index

# If assessment is ongoing
if current_index < len(selected_items):
    item = selected_items[current_index]
    st.subheader(f"{selected_goal} ({current_index + 1}/{len(selected_items)})", divider="blue")

    # Show image if available
    if "image" in item and pd.notna(item["image"]) and item["image"].strip():
        st.image(item["image"], width=300)

    # Show additional instruction text if available
    if "text" in item and pd.notna(item["text"]) and item["text"].strip():
        st.info(item["text"])

    # Always show the question
    if "question" in item and pd.notna(item["question"]) and item["question"].strip():
        st.markdown(f"**{item['question']}**")
    else:
        st.warning("⚠️ No question text found for this item.")


    # TextInput bleibt immer sichtbar
    user_answer = st.text_input("Enter your answer here:", key=f"input_{current_index}")

    # Funktion zum Absenden der Antwort und Generieren von Feedback
    def submit_answer():
        feedback = generate_feedback(
            text=item["text"],
            question=item["question"],
            correct_response=item["correct_answer"],
            student_response=user_answer,
            feedback_prompt=item["feedback_prompt"]
        )
        st.session_state.last_feedback = feedback
        st.session_state.last_correct = item["correct_answer"]
        st.session_state.last_user_answer = user_answer
        st.session_state.show_feedback = True
        st.rerun()

    # Buttons je nach Zustand
    if not st.session_state.show_feedback:
        if st.button("Submit Answer"):
            submit_answer()
    else:
        # Feedback anzeigen
        st.success(st.session_state.last_feedback)
        # Zwei Optionen: nochmal absenden oder weiter
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Resubmit answer"):
                submit_answer()
        with col2:
            if st.button("Next"):
                st.session_state.question_index += 1
                st.session_state.show_feedback = False
                st.rerun()

# If all questions completed
else:
    st.success("🎉 Assessment complete! Well done.")
    if st.button("Restart"):
        for key in [
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
        st.rerun()

