import re

def extract_mcqs(text):
    lines = text.splitlines()
    mcqs = []
    current_question = None
    current_options = {}
    user_answer = None
    question_number = 1
    i = 0

    while i < len(lines):
        line = lines[i].strip()

       
        if re.match(rf"^(س?{question_number})[\.\)]", line) or re.match(rf"^{question_number}[\.\)]", line):
            # Save the previous question
            if current_question and current_options:
                mcqs.append({
                    "question": current_question,
                    "options": current_options,
                    "user_answer": user_answer
                })
                current_question = None
                current_options = {}
                user_answer = None

            current_question = line
            question_number += 1
            i += 1
            continue

        # Match options: A), B), C), D)
        option_match = re.match(r"([A-D])\)\s*(.*)", line)
        if option_match:
            option_label = option_match.group(1).upper()
            option_text = option_match.group(2)
            current_options[option_label] = option_text
            i += 1
            continue

      
        user_line_match = re.search(r"User Selected:\s*([A-D])\)", line)
        if user_line_match:
            user_answer = user_line_match.group(1).upper()

        i += 1

  
    if current_question and current_options:
        mcqs.append({
            "question": current_question,
            "options": current_options,
            "user_answer": user_answer
        })

    return mcqs
