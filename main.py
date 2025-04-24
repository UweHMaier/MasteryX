import streamlit as st
import uuid
#from firebase_config import database_ref

# --- Set page config ---
st.set_page_config(page_title="MasteryX", layout="centered")

# --- Init state for one session ---
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

if "user" not in st.session_state:
    st.session_state["user"] = "Demo-User"

# --- Page setup ---
goals_page = st.Page(
    page="views/goals.py",
    title="Learning Goals",
    default=True,
)
assessment_page = st.Page(
    page="views/assessment.py",
    title="Assessment",
)

# --- Navigation Menu ---
pg = st.navigation(pages=[goals_page, assessment_page])

# --- Shared on all pages ---
st.logo("images/masteryx.jpg")
st.sidebar.markdown("### MasteryX-APP")
st.sidebar.markdown(f"👋 Hello {st.session_state['user']}!")
st.sidebar.markdown(f"🆔 Session-ID: `{st.session_state['session_id']}`")

# --- Run the selected page ---
pg.run()


