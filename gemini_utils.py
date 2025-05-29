# gemini_utils.py
import google.generativeai as genai
import streamlit as st
import os
from dotenv import load_dotenv

# Load the API key once
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Init model once
model = genai.GenerativeModel("gemini-1.5-flash")



def generate_feedback(question: str, correct_response: str, student_response: str) -> str:

    prompt = (
        f"You are a helpful and encouraging tutor for secondary students."
        f"Please write a short and encouraging feedback to the student."
        f"Keep the response short (max 50 words) and speak directly to the student using 'you'."
        f"This is a quiz question: {question}."
        f"This is the correct answer: {correct_response}."
        f"This is the student answer: {student_response}."
    )

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        error_message = str(e).lower()
        if "quota" in error_message or "rate limit" in error_message:
            st.warning("🚨 Too many requests. Please wait a few seconds and try again.")
        else:
            st.error(f"Gemini API error: {e}")
        return None
