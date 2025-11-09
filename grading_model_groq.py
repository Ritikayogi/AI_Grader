"""
grading_model_groq.py
Automated test-grading script using Groq (LLaMA 3.1 8B Instant Model).
"""

import os
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv
from groq import Groq
import re

# Load environment variables (API key)
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- Helper function to extract marks ----------------
def extract_marks_reason(text, max_marks=5):
    """
    Extract marks and reason from model response text.
    Example: "Marks: 4/5\nReason: Good explanation but missed one point."
    """
    marks_pattern = r"(\d+(\.\d+)?)(?=\s*/?\s*5|\b)"
    reason_pattern = r"(?i)reason[:\-–]\s*(.*)"

    marks_match = re.search(marks_pattern, text)
    reason_match = re.search(reason_pattern, text)

    marks = float(marks_match.group(1)) if marks_match else 0
    if marks > max_marks:
        marks = max_marks

    reason = reason_match.group(1).strip() if reason_match else "No clear reason found."
    return marks, reason


# ---------------- Main Grading Function ----------------
def grade_answers(input_file, output_file):
    print("📘 Loading dataset...")
    df = pd.read_excel(input_file)

    results = []

    for i, row in tqdm(df.iterrows(), total=len(df)):
        question = str(row.get("Question", ""))
        ideal_answer = str(row.get("Ideal_Answer", ""))
        student_answer = str(row.get("Student_Answer", ""))
        max_marks = row.get("Max_Marks", 5)

        # Skip if data missing
        if not question or not ideal_answer or not student_answer:
            results.append({
                "Question_ID": f"Q{i+1}",
                "Question": question,
                "GPT_Marks": 0,
                "Max_Marks": max_marks,
                "GPT_Reason": "⚠️ Missing data."
            })
            continue

        # Prompt to model
        prompt = f"""
You are a teacher grading a student's short answer.

Question: {question}
Ideal Answer: {ideal_answer}
Student Answer: {student_answer}

Give marks (out of {max_marks}) and explain shortly.

Format:
Marks: <number>/<max_marks>
Reason: <short reason>
"""

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            content = response.choices[0].message.content.strip()
            marks, reason = extract_marks_reason(content, max_marks)

        except Exception as e:
            marks, reason = 0, f"❌ API Error: {e}"

        results.append({
            "Question_ID": f"Q{i+1}",
            "Question": question,
            "GPT_Marks": marks,
            "Max_Marks": max_marks,
            "GPT_Reason": reason
        })

    # Save output
    graded_df = pd.DataFrame(results)
    graded_df.to_excel(output_file, index=False)
    print(f"\n✅ Done! Results saved to {output_file}")


# ---------------- Script Entry Point ----------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI Grader using Groq API")
    parser.add_argument("--input", type=str, required=True, help="Path to input Excel file")
    parser.add_argument("--output", type=str, required=True, help="Path to save graded output")
    args = parser.parse_args()

    grade_answers(args.input, args.output)

