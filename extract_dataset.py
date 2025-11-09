import pdfplumber
import pandas as pd
import re

QP_FILE = "Maanya_140425_QP.pdf"
MS_FILE = "Maanya_140425_MS.pdf"
CP_FILE = "Maanya_140425_CP.pdf"

def extract_text(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text

print("📘 Extracting text from PDFs...")
qp_text = extract_text(QP_FILE)
ms_text = extract_text(MS_FILE)
cp_text = extract_text(CP_FILE)
print("✅ PDFs loaded successfully!")

# Pattern updated for “Answer 1”, “Q1”, etc.
def split_blocks(text):
    parts = re.split(r"(?:\n|^)(?:Q(?:uestion)?\s*\d+[\.\):]?|Answer\s*\d+[\.\):]?)", text)
    blocks = [p.strip() for p in parts if len(p.strip()) > 20]
    return blocks

qp_questions = split_blocks(qp_text)
ms_answers = split_blocks(ms_text)
cp_answers = split_blocks(cp_text)

print(f"📄 Found {len(qp_questions)} questions in QP.")
print(f"📗 Found {len(ms_answers)} ideal answers in MS.")
print(f"📕 Found {len(cp_answers)} student answers in CP.")

rows = []
for i in range(min(len(qp_questions), len(ms_answers), len(cp_answers))):
    rows.append({
        "Question_ID": f"Q{i+1}",
        "Question": qp_questions[i],
        "Ideal_Answer": ms_answers[i],
        "Student_Answer": cp_answers[i],
        "Max_Marks": 5
    })

if not rows:
    print("⚠️ No matching rows found. Try adjusting regex or check PDF formatting.")
else:
    df = pd.DataFrame(rows)
    df.to_excel("training_data.xlsx", index=False)
    print("✅ training_data.xlsx created successfully!")

