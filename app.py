# app.py
import streamlit as st
import subprocess
import os
import tempfile
from pathlib import Path

st.set_page_config(page_title="AI Grader (Demo)", page_icon="🧾", layout="centered")

st.title("AI Auto-Grader — Demo")
st.markdown("""
Upload the extracted dataset Excel (`training_data_all.xlsx`) or any similar Excel with columns:
**Question, Ideal_Answer, Student_Answer, Max_Marks (optional)**.  
The app will run the grading script (Groq / Llama) and return a graded Excel.
""")

st.sidebar.header("Instructions")
st.sidebar.markdown("""
1. Put your Groq API key in environment variable `GROQ_API_KEY` (or start Streamlit from terminal with it exported).  
2. Make sure `grading_model_groq.py` is present in the same folder and is the working script you've tested.  
3. Upload dataset (Excel). Click **Grade** and wait — results will be available to download.
""")

uploaded = st.file_uploader("Upload input Excel (training_data_all.xlsx or similar)", type=["xlsx","xls"], accept_multiple_files=False)

out_name = st.text_input("Output filename (will be saved in app folder)", value="graded_output_streamlit.xlsx")

run_button = st.button("Grade")

# Helper to save uploaded file to disk
def save_uploaded(uploaded_file, save_path: Path):
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return save_path

# Run grading using existing script via subprocess
def run_grader(input_path: str, output_path: str):
    # Use same python that runs streamlit (assumes venv activated when launching streamlit)
    python_exe = os.getenv("PYTHON_EXECUTABLE", "python")
    cmd = [python_exe, "grading_model_groq.py", "--input", input_path, "--output", output_path]
    # Run and stream output
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr

if run_button:
    if not uploaded:
        st.warning("Please upload an Excel file first.")
    else:
        tmpdir = Path(tempfile.mkdtemp(prefix="ai_grader_"))
        input_path = tmpdir / "uploaded_input.xlsx"
        output_path = tmpdir / out_name

        save_uploaded(uploaded, input_path)
        st.info(f"Saved upload to `{input_path}` — starting grading...")

        with st.spinner("Grading in progress. This can take a few seconds per question..."):
            code, sout, serr = run_grader(str(input_path), str(output_path))

        if code == 0 and output_path.exists():
            st.success(f"Grading completed — saved to `{output_path.name}`")
            with open(output_path, "rb") as f:
                st.download_button("Download graded Excel", f, file_name=output_path.name)
            # Show a preview of first few rows using pandas
            try:
                import pandas as pd
                df = pd.read_excel(output_path)
                st.write("Preview (first 8 rows):")
                st.dataframe(df.head(8))
            except Exception as e:
                st.warning(f"Could not show preview: {e}")
            # show logs if any
            if sout.strip():
                st.text_area("Grader stdout", sout, height=120)
            if serr.strip():
                st.text_area("Grader stderr", serr, height=120)
        else:
            st.error("Grading failed. See error details below.")
            st.text_area("stderr", serr or "No stderr output", height=200)
            st.text_area("stdout", sout or "No stdout output", height=200)

