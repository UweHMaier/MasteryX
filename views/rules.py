import streamlit as st

# Validate topic and goal selection
if not st.session_state.get("topic") or not st.session_state.get("goal"):
    st.error("Please select a topic and goal first.")
    st.stop()

# Fetch selected goal
selected_topic = st.session_state["topic"]
selected_goal = st.session_state["goal"]
df_rules = st.session_state["df_rules"]
rule = df_rules.loc[(df_rules["topic"] == selected_topic) & (df_rules["goal"] == selected_goal), "rule"].values[0]

# UI
st.subheader(f"{selected_topic}: {selected_goal}")
st.info(f"{rule}")

# Button to assessment
if st.button("Go to the quiz"):
    st.switch_page("views/assessment.py")