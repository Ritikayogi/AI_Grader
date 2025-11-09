import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io, pandas as pd, re

QP_FILE = "Maanya_140425_QP.pdf"
MS_FILE = "Maanya_140425_MS.pdf"
CP_FILE = "Maanya_140425_CP.pdf"

def ocr_extract(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=200)
        img = Image.open(io.BytesIO(pix.tobytes()))
        txt = pytesseract.image_to_string(img)
        text += f"\n--- Page {i+1} ---\n" + txt
    return text

print("📘 Running OCR text extraction...")
qp_text = ocr_extract(QP_FILE)
ms_text = ocr_extract(MS_FILE)
cp_text = ocr_extract(CP_FILE)
print("✅ OCR extraction done!")

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
    print("⚠️ No matching rows found — check extracted text manually.")
else:
    df = pd.DataFrame(rows)
    df.to_excel("training_data_ocr.xlsx", index=False)
    print("✅ training_data_ocr.xlsx created successfully!")

