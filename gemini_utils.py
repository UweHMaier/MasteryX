# gemini_utils.py
import google.generativeai as genai
import streamlit as st
import os
import json
import re
from dotenv import load_dotenv

# Load the API key once
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Init model once
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_test_items(subject: str, goal: str, hobby: str) -> list:
    """
    Sends a prompt to Gemini to generate 5 test items (questions and correct answers)
    based on subject, learning goal, and extra info.
    
    Returns: List of dictionaries:
    [
        {
            "question": "Question text here",
            "solution": "Correct answer here"
        },
        ...
    ]
    """
    if not subject or not goal or not hobby:
        return []

    prompt = (
        f"You are a teacher creating quiz questions for a student.\n"
        f"Subject: {subject}\n"
        f"Learning goal: {goal}\n"
        f"Additional context or topic: {hobby}\n\n"
        f"Generate 5 short-answer test questions for this context.\n"
        f"Each question should be clear and answerable in a single word or short phrase.\n"
        f"Return your response ONLY as a valid JSON list with the following format:\n\n"
        f"[\n"
        f"  {{\n"
        f"    \"question\": \"Your question text here\",\n"
        f"    \"solution\": \"Correct answer\"\n"
        f"  }},\n"
        f"  ... (4 more)\n"
        f"]\n\n"
        f"Important:\n"
        f"- Only return valid JSON.\n"
        f"- Do not add any explanation, introduction, or extra text."
    )

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if match:
            json_str = match.group(0)
            test_items = json.loads(json_str)
            return test_items
        else:
            st.warning("No valid JSON found in Gemini's response.")
            return []

    except Exception as e:
        st.error(f"Gemini error during test item generation: {e}")
        return []


def generate_overall_feedback(responses: list) -> str:
    """
    Sends the full list of questions, correct solutions, and student answers
    to Gemini and receives a single paragraph of feedback.

    Returns:
        A short, encouraging feedback message as a string.
    """

    # Format the input as structured text for Gemini
    formatted = "\n\n".join(
        f"Q{i+1}: {r['question']}\n"
        f"Correct Answer: {r['solution']}\n"
        f"Student Answer: {r['user_answer'] or '[No answer]'}"
        for i, r in enumerate(responses)
    )

    prompt = (
        f"You are a helpful and encouraging tutor.\n\n"
        f"Here is a student's quiz performance with questions, correct answers, and their responses:\n\n"
        f"{formatted}\n\n"
        f"Please write overall feedback for the student. Focus on:\n"
        f"- Accuracy of answers\n"
        f"- Common errors or misunderstandings (if any)\n"
        f"- One motivational sentence to end with\n\n"
        f"Keep the response short (max 100 words) and speak directly to the student using 'you'."
    )

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return f"⚠️ Gemini error: {e}"
