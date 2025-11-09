import os
import pandas as pd
from openai import OpenAI
from tqdm import tqdm
from dotenv import load_dotenv
import re

# ---------------------------
# Load environment variables
# ---------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ No API key found. Please set OPENAI_API_KEY in your .env file or export it manually.")

client = OpenAI(api_key=api_key)

# ---------------------------
# Function to extract marks safely
# ---------------------------
def extract_marks_reason(text, max_marks=5):
    """Extract marks and reason even if GPT format is irregular"""
    marks, reason = 0, ""
    try:
        # 1️⃣ Try finding pattern like: Marks: 4.5 or Marks awarded: 3
        match = re.search(r"[Mm]arks[^0-9]*(\d+(\.\d+)?)", text)
        if match:
            marks = float(match.group(1))
        else:
            # 2️⃣ Extract any number in range (0–max_marks)
            nums = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", text)]
            if nums:
                marks = max(0, min(max(nums), max_marks))
        # 3️⃣ Extract reason text if available
        reason_match = re.search(r"[Rr]eason[^:]*[:\-]?\s*(.*)", text)
        if reason_match:
            reason = reason_match.group(1).strip()
        else:
            reason = text.strip()[:200]
    except Exception as e:
        reason = f"⚠️ Parse error: {e}"
    return round(marks, 2), reason

# ---------------------------
# Core grading logic
# ---------------------------
def grade_answers(input_file, output_file):
    print("📘 Loading dataset...")
    df = pd.read_excel(input_file)

    if not {"Question", "Ideal_Answer", "Student_Answer"}.issubset(df.columns):
        raise ValueError("Excel must have columns: Question, Ideal_Answer, Student_Answer")

    results = []

    print("🤖 Sending answers to GPT for grading...\n")

    for i, row in tqdm(df.iterrows(), total=len(df)):
        question = str(row["Question"])
        ideal_answer = str(row["Ideal_Answer"])
        student_answer = str(row["Student_Answer"])
        max_marks = row["Max_Marks"] if "Max_Marks" in row else 5

        prompt = f"""
You are an experienced teacher grading student answers.

Grade the student's response based on the ideal answer and question.

Question:
{question}

Ideal Answer:
{ideal_answer}

Student Answer:
{student_answer}

Now respond in this exact format:
Marks: <number between 0 and {max_marks}>
Reason: <one short line why you gave that mark>
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )

            content = response.choices[0].message.content.strip()
            marks, reason = extract_marks_reason(content, max_marks)

        except Exception as e:
            marks, reason = 0, f"❌ API Error: {str(e)}"

        results.append({
            "Question_ID": f"Q{i+1}",
            "Question": question,
            "GPT_Marks": marks,
            "Max_Marks": max_marks,
            "GPT_Reason": reason
        })

    out_df = pd.DataFrame(results)
    out_df.to_excel(output_file, index=False)
    print(f"\n✅ Done! Results saved to {output_file}")

# ---------------------------
# Run from terminal
# ---------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Stable AI Grading Model (GPT-4o-mini)")
    parser.add_argument("--input", required=True, help="Input Excel file")
    parser.add_argument("--output", required=True, help="Output Excel file")
    args = parser.parse_args()
    grade_answers(args.input, args.output)

