import os
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

df = pd.read_excel("training_data_all.xlsx")

with open("groq_raw_log.txt", "w") as f:
    for i, row in df.head(5).iterrows():  # first 5 questions
        q = str(row["Question"])
        ideal = str(row["Ideal_Answer"])
        stu = str(row["Student_Answer"])
        prompt = f"""
You are grading a student answer.

Question: {q}
Ideal Answer: {ideal}
Student Answer: {stu}

Please respond in 2 lines:
Marks (out of 5): <number>
Reason: <short explanation>
"""
        try:
            resp = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
            )
            content = resp.choices[0].message.content.strip()
        except Exception as e:
            content = f"❌ API Error: {e}"

        print(f"Q{i+1} → {content[:100]}...")
        f.write(f"\n--- Q{i+1} ---\n{content}\n")

print("✅ Done. Check 'groq_raw_log.txt' for full responses.")

