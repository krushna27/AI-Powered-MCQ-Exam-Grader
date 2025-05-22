import streamlit as st
from PyPDF2 import PdfReader
from grader.parser import extract_mcqs
from grader.gemini import predict_answer
import fitz
st.title("AI-Powered MCQ Exam Grader")

uploaded_file = st.file_uploader("Upload your MCQ exam PDF", type=["pdf"])




if uploaded_file is not None: 
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    #Loop through each page and extract text.
    text = ""
    for page in doc:
        text += page.get_text()

    mcqs = extract_mcqs(text)
    st.subheader("🔍 Parsed MCQs Preview")
    st.json(mcqs)

    with st.spinner("Predicting correct answers using Gemini..."):
        for q in mcqs:
            try:
                prediction = predict_answer(q["question"], q["options"])
                q["predicted_answer"] = prediction
            except Exception as e:
                q["predicted_answer"] = "Error"
                st.error(f"Gemini API error: {e}")

    # Grade
    correct_count = 0
    for q in mcqs:
        user = str(q.get("user_answer", "")).strip().upper()
        predicted = q.get("predicted_answer", "").strip().upper()
        q["is_correct"] = user == predicted
        if q["is_correct"]:
            correct_count += 1

    st.subheader("📋 Grading Report")
    for idx, q in enumerate(mcqs):
        st.markdown(f"### Q{idx + 1}: {q['question']}")
        for key, val in q["options"].items():
            st.markdown(f"- {key}) {val}")
        st.markdown(f"✅ **Gemini Predicted:** `{q['predicted_answer']}`")
        st.markdown(f"🧑 **User Selected:** `{q['user_answer']}`")
        if q["is_correct"]:
            st.success("✅ Correct")
        else:
            st.error("Incorrect")
        st.markdown("---")

    st.subheader("Summary")
    total = len(mcqs)
    st.markdown(f"- all Questions: **{total}**")
    st.markdown(f"- Correct: **{correct_count}**")
    st.markdown(f"- Wrong: **{total - correct_count}**")
    st.markdown(f"- Total Score: **{correct_count}/{total}**")
else:
    st.info("📥 Upload a file.")
