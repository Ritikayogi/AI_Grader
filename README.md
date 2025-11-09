🤖 AI Auto-Grader
🎯 Project Overview

The AI Auto-Grader is an intelligent system that automatically evaluates and grades students’ answers by comparing them with ideal solutions.
It uses Groq’s Llama-3.1 large language model to assess the correctness, completeness, and reasoning quality of a student’s response — and assigns marks accordingly.

This project was developed as a demonstration of how Generative AI can automate academic grading efficiently and consistently.

⚙️ Tech Stack
Component	Technology Used
AI Model	Groq Llama-3.1 (via Groq API)
Programming Language	Python 3.13
Frontend Interface	Streamlit
Text Extraction	Tesseract OCR, pdfplumber
Data Handling	Pandas, OpenPyXL
File Format	XLSX (Excel Dataset)
🧠 How It Works

Extracts questions, ideal answers, and student answers from PDFs or Excel sheets.

Sends each question–answer pair to Groq’s Llama-3.1 model.

The model evaluates the response for:

Concept understanding

Accuracy and completeness

Depth of reasoning

Returns:

✅ Marks obtained

💬 Reason for grading

Stores all results into a structured Excel file: graded_output_groq.xlsx.

📂 Folder Structure
AI_Grader/
├── app.py                     # Streamlit web interface
├── grading_model_groq.py      # Core AI grading logic using Groq
├── extract_dataset_ocr.py     # Extracts text from PDFs (QP, MS, CP)
├── training_data_all.xlsx     # Dataset: Questions + Answers
├── requirements.txt           # Python dependencies
├── README.md                  # Documentation file (this one)
├── Maanya_*.pdf               # Sample Question/Mark Scheme/Checked Papers
└── graded_output_groq.xlsx    # AI-generated results

🚀 Run Locally
1️⃣ Clone or Extract the Project

If using GitHub:

git clone https://github.com/Ritikayogi/AI_Grader.git
cd AI_Grader


If using ZIP:

Unzip AI_Grader.zip

Open the folder in terminal or VS Code

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Add Your Groq API Key

Create a file named .env in the same directory and add:

GROQ_API_KEY = "your_groq_api_key_here"

4️⃣ Run the AI Grader
python grading_model_groq.py --input "training_data_all.xlsx" --output "graded_output.xlsx"


After execution, the system will generate a new file:

graded_output.xlsx


containing marks and reasoning for each answer.

🖥️ (Optional) Run the Streamlit Web App

You can also use the project with a clean web UI.

streamlit run app.py


Then open the link shown in your terminal (usually http://localhost:8501
).
Upload your Excel dataset → click Grade Answers → view results interactively.

🧪 Example Output
Question	Ideal_Answer	Student_Answer	Marks	Reasoning
Q1	Explain Binomial Theorem.	A binomial expansion shows combinations...	3/4	Answer mostly correct, missed one detail.
Q2	Define Normal Distribution.	It shows a bell-shaped curve.	1/2	Too short, lacks proper reasoning.
💡 Key Features

✅ Works for any subject (Math, Science, etc.)
✅ Reads answers from PDFs or Excel files
✅ Uses Groq Llama-3.1 for high-speed evaluation
✅ Generates detailed reasoning with marks
✅ Easy to extend for future fine-tuning

🧑‍💻 Author

Ritika Yogi
📧 yogiritika02@gmail.com

💼 GitHub: Ritikayogi

🏁 Future Improvements

Add automatic question type detection (MCQ / Subjective / Numerical)

Improve scoring logic for long answers

Add analytics dashboard (accuracy, average score trends)

Support batch grading across multiple subjects

🧩 Sample Run Commands

For quick testing:

# Extract data from PDFs (if needed)
python extract_dataset_ocr.py

# Run the AI grading model
python grading_model_groq.py --input "training_data_all.xlsx" --output "graded_output_groq.xlsx"

🧭 Project Workflow Diagram
PDF / Excel
     │
     ▼
 Extract Text (OCR / pdfplumber)
     │
     ▼
 Compare → Groq Llama-3.1 Model
     │
     ▼
 Generate Marks + Reasoning
     │
     ▼
 Save as graded_output.xlsx

🏆 Result

A fully functional AI-powered automated grading system
that can check descriptive answers, give scores, and explain its reasoning —
reducing manual checking time by over 80% ⚡
