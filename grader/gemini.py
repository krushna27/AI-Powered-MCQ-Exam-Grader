


import os
import google.generativeai as genai



API_KEY = "AIzaSyDyHQdtNp-4Lwrb9aTikttNfSbNeVRuADs"
genai.configure(api_key=API_KEY)

def predict_answer(question_text, options_dict):
    prompt = build_prompt(question_text, options_dict)
    model = genai.GenerativeModel("gemini-2.0-flash-lite")
    response = model.generate_content(prompt)
    return response.text.strip()

def build_prompt(question, options):
    prompt = f"""You are an expert in multiple-choice exams. Choose the correct answer from the options till data May 2025 provided below.
    also based on user selected answer(A,B,C,D) see from the marks answer what answer his is selected whether it is in english or arabic.

Question:
{question}

Options:
"""
    for key in sorted(options.keys()):
        prompt += f"{key}) {options[key]}\n"

    prompt += "\nReturn only the correct option letter (A, B, C, or D)."
    return prompt
