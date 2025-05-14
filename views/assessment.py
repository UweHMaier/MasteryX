import streamlit as st
from content import content
from gemini_utils import generate_feedback

# Validate topic and goal selection
if not st.session_state.get("topic") or not st.session_state.get("goal"):
    st.error("Please select a topic and goal first.")
    st.stop()

# Fetch selected goal
selected_topic = st.session_state["topic"]
selected_goal_name = st.session_state["goal"]
goal_data = next(goal for goal in content[selected_topic]["goals"] if goal["name"] == selected_goal_name)
test_items = goal_data["test_items"]

# Initialize state
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "show_feedback" not in st.session_state:
    st.session_state.show_feedback = False
if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = ""
if "last_correct" not in st.session_state:
    st.session_state.last_correct = ""
if "last_question" not in st.session_state:
    st.session_state.last_question = ""
if "last_user_answer" not in st.session_state:
    st.session_state.last_user_answer = ""

current_index = st.session_state.question_index

st.title(f"Assessment: {selected_goal_name}")
st.markdown(f"**Rule:** {goal_data['rule']}")
st.divider()

# If assessment is ongoing
if current_index < len(test_items):
    item = test_items[current_index]
    st.subheader(f"Question {current_index + 1} of {len(test_items)}")
    user_answer = st.text_input(item["question"], key=f"input_{current_index}")

    if st.button("Submit Answer"):
        feedback = generate_feedback(
            question=item["question"],
            correct_response=item["correct_answer"],
            student_response=user_answer
        )
        st.session_state.last_feedback = feedback
        st.session_state.last_correct = item["correct_answer"]
        st.session_state.last_question = item["question"]
        st.session_state.last_user_answer = user_answer
        st.session_state.show_feedback = True

    if st.session_state.show_feedback:
        st.markdown("### Feedback")
        st.markdown(f"**Question:** {st.session_state.last_question}")
        st.markdown(f"- Your answer: {st.session_state.last_user_answer}")
        st.markdown(f"- Correct answer: {st.session_state.last_correct}")
        st.markdown(f"- Feedback: {st.session_state.last_feedback}")
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
