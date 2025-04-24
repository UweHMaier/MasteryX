import streamlit as st
from gemini_utils import generate_test_items, generate_overall_feedback


# --- Page logic ---
st.title("Assessment")

for key, value in {
    "topic": None,
    "goal": None,
    "extra": None,
    "responses": [],
    "current_index": 0,
    "show_feedback": False,
    "feedback": ""
}.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- Check required state ---
required_keys = ["topic", "goal"]
if not all(st.session_state.get(k) for k in required_keys):
    st.warning("Please go to the 'Set Learning Goal' page first and make your selections.")
    st.stop()

st.success(f"This is a short quiz on {st.session_state.goal} in {st.session_state.topic} ")

# --- Initialize assessment state ---
if "test_items" not in st.session_state or not st.session_state["test_items"]:
    extra = st.session_state["extra"] or "currently no extra information"
    st.session_state["test_items"] = generate_test_items(
        st.session_state["topic"],
        st.session_state["goal"],
        extra
    )
    st.session_state["responses"] = [
        {"question": item["question"], "solution": item["solution"], "user_answer": ""}
        for item in st.session_state["test_items"]
    ]
    st.session_state["current_index"] = 0
    st.session_state["show_feedback"] = False


# --- Show current question ---
index = st.session_state.current_index
items = st.session_state.test_items
responses = st.session_state.responses

if index < len(items):
    st.subheader(f"Question {index + 1} of {len(items)}")
    st.write(items[index]["question"])

    # Text input for user answer
    user_input = st.text_input("Your answer:", value=responses[index]["user_answer"], key=f"answer_{index}")

    if st.button("Next"):
        st.session_state.responses[index]["user_answer"] = user_input
        st.session_state.current_index += 1
        st.rerun()
else:
    # All questions answered — show feedback
    if not st.session_state.show_feedback:
        st.session_state.feedback = generate_overall_feedback(st.session_state.responses)
        st.session_state.show_feedback = True

    st.subheader("Assessment Complete!")
    st.write(st.session_state.feedback)
    st.balloons()

if st.session_state.get("show_feedback"):
    # --- Reset assessment only ---
    if st.button("🔁 Restart This Assessment"):
        for key in ["test_items", "responses", "current_index", "show_feedback", "feedback"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    # --- Go back to learning goals page ---
    if st.button("🏁 Start Over (Set Learning Goals Again)"):
        for key in ["topic", "goal", "extra", "test_items", "responses", "current_index", "show_feedback", "feedback"]:
            if key in st.session_state:
                del st.session_state[key]
        st.switch_page("views/goals.py")  # Change this to the actual filename of your goals page