import streamlit as st
import uuid
import pandas as pd


# Import topic, learning goals and quizitems from google sheets
sheet_quizitems = "https://docs.google.com/spreadsheets/d/1oX82oxkG0TMFHSF0VsYt_7Jjlmd1zc7YPWqWNqhR6q8/export?format=csv"
try:
    df_quizitems = pd.read_csv(sheet_quizitems, quotechar='"', on_bad_lines='skip')
except Exception as e:
    st.error("Failed to load data from Google Sheets.")
    st.stop()

# Import topic, goals, and rules from google sheets
sheet_rules = "https://docs.google.com/spreadsheets/d/1Bhi8indbSHAtedAjxqHD0WqE9FJM0EOcukOyypBvSwA/export?format=csv"
try:
    df_rules = pd.read_csv(sheet_rules, quotechar='"', on_bad_lines='skip')
except Exception as e:
    st.error("Failed to load data from Google Sheets.")
    st.stop()


# --- Set page config ---
st.set_page_config(page_title="MasteryX", layout="centered")

# -- Init session state ---
for key, default in {
    "user": "Demo-User",
    "session_id": str(uuid.uuid4()),
    "topic": None,
    "goal": None,
    "df_quizitems": df_quizitems,
    "df_rules": df_rules,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# --- Page setup ---
goals_page = st.Page(
    page="views/goals.py",
    title="Learning Goals",
    default=True,
)
rules_page = st.Page(
    page="views/rules.py",
    title="Rules",
)
assessment_page = st.Page(
    page="views/assessment.py",
    title="Assessment",
)

# --- Navigation Menu ---
pg = st.navigation(pages=[goals_page, rules_page, assessment_page])

# --- Shared on all pages ---
st.logo("images/masteryx.jpg")

# --- Run the selected page ---
pg.run()


