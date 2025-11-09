import fitz
import pytesseract
from PIL import Image
import io, os, pandas as pd, re

# Folder path
PDF_DIR = "."

def ocr_extract(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=200)
        img = Image.open(io.BytesIO(pix.tobytes()))
        txt = pytesseract.image_to_string(img)
        text += f"\n--- Page {i+1} ---\n" + txt
    return text

def split_blocks(text):
    parts = re.split(r"(?:\n|^)(?:Q(?:uestion)?\s*\d+[\.\):]?|Answer\s*\d+[\.\):]?)", text)
    return [p.strip() for p in parts if len(p.strip()) > 20]

def process_topic(topic_prefix):
    qp_file = f"{topic_prefix}_QP.pdf"
    ms_file = f"{topic_prefix}_MS.pdf"
    cp_file = f"{topic_prefix}_CP.pdf"

    if not all(os.path.exists(f) for f in [qp_file, ms_file, cp_file]):
        print(f"⚠️ Missing files for topic {topic_prefix}")
        return None

    print(f"\n📘 Processing topic: {topic_prefix}")
    qp_text = ocr_extract(qp_file)
    ms_text = ocr_extract(ms_file)
    cp_text = ocr_extract(cp_file)

    qp_questions = split_blocks(qp_text)
    ms_answers = split_blocks(ms_text)
    cp_answers = split_blocks(cp_text)

    rows = []
    for i in range(min(len(qp_questions), len(ms_answers), len(cp_answers))):
        rows.append({
            "Topic": topic_prefix,
            "Question_ID": f"Q{i+1}",
            "Question": qp_questions[i],
            "Ideal_Answer": ms_answers[i],
            "Student_Answer": cp_answers[i],
            "Max_Marks": 5
        })
    return pd.DataFrame(rows)

def main():
    topics = sorted(set("_".join(f.split("_")[:2]) for f in os.listdir(PDF_DIR) if f.endswith("_QP.pdf")))
    print(f"🧩 Detected topics: {topics}")

    all_data = []
    for t in topics:
        df = process_topic(t)
        if df is not None and not df.empty:
            all_data.append(df)

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        final_df.to_excel("training_data_all.xlsx", index=False)
        print("\n✅ All topics processed! Saved to training_data_all.xlsx")
    else:
        print("\n⚠️ No valid data extracted. Check PDF names and quality.")

if __name__ == "__main__":
    main()

