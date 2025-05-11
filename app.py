import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Resume Cretique", page_icon="📃", layout="centered")
st.title("Resume Critique App")
st.markdown("Upload your resume and get AI-powered feedback toiled in your needs!")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

upload_file = st.file_uploader("Upload Resume", type=["pdf", "txt"])
job_role = st.text_input("Enter Job Role you're targgeting (optional)")
analyze = st.button("Analyze Resume")

def extend_file_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extend_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extend_file_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

if analyze and upload_file:
    try:
        file_content = extend_text_from_file(upload_file)
        if not file_content.strip():
            st.error("file does not have any content...........")
            st.stop()
        
        prompt = f""" Please analyze this and provide constructive feedback.
        Focus on the following aspect:
        1) Content clarity and impact
        2) Skills presentation
        3) Experience description
        4) Specific improvements for {job_role if job_role else 'general job applications'}
        Resume Content: {file_content}
        Please provide your analysis in a clear, structured format with specific recommandations
        """
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role":"system", "content":"you are an expert resume reviewer with year of experience"},
                {"role":"user", "content":prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        st.markdown("### Analysis Result")
        st.markdown(response.choices[0].message.content)
    except Exception as e:
        st.error(f"an error occurred {str(e)}")
