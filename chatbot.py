# File: chatbot.py

import os
import streamlit as st
from PyPDF2 import PdfReader
import requests
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# GroqCloud API Configuration
GROQCLOUD_API_KEY = os.getenv("GROQCLOUD_API_KEY")  # Get the API key from environment variables
GROQCLOUD_API_URL = "https://api.groq.com/openai/v1/chat/completions"
CHATGROQ_MODEL = "mixtral-8x7b-32768"  # ChatGroq model to use


# Helper function: Extract text from PDF
def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
        return text
    except Exception as e:
        return f"Error extracting text: {e}"


# Helper function: Split text using LangChain
def split_resume_text(text):
    splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200)
    return splitter.split_text(text)


# Helper function: Call GroqCloud API
def call_groqcloud(prompt):
    if not GROQCLOUD_API_KEY:
        return "Error: API key is missing. Please set the GROQCLOUD_API_KEY environment variable."

    headers = {
        "Authorization": f"Bearer {GROQCLOUD_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": CHATGROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(GROQCLOUD_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error calling GroqCloud: {e}"


# Streamlit UI
def main():
    st.title("AI Resume Chatbot 🤖")
    st.write("Hi, I'm your Resume Analyser Bot! Please upload your resume to get started.")

    # File upload
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

    if uploaded_file:
        # Save the uploaded file
        file_path = os.path.join("temp", uploaded_file.name)
        os.makedirs("temp", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")

        # Extract resume text
        resume_text = extract_text_from_pdf(file_path)
        if not resume_text.strip():
            st.error("Failed to extract text from the resume. Please upload a valid PDF.")
            return

        # Split resume text into manageable chunks using LangChain
        chunks = split_resume_text(resume_text)

        st.write("### Resume Analysis Complete! What would you like to do next?")
        st.write("1. Resume Analysis")
        st.write("2. Job Recommendations")
        st.write("3. Job Matching")

        # User action
        action = st.selectbox("Choose an action:", ["", "Resume Analysis", "Job Recommendations", "Job Matching"])

        if action == "Resume Analysis":
            # Prepare analysis prompt
            analysis_prompt = f"""
            Analyze the following resume and extract key details:
            - Name
            - Contact information
            - Email address
            - Education
            - Work experience
            - Skills
            - Certifications
            Provide a detailed analysis of the candidate's strengths, weaknesses, and areas for improvement. Also, give a rating out of 10.
            
            Resume Content:
            {resume_text}
            """
            analysis_feedback = call_groqcloud(analysis_prompt)
            st.write("### Resume Analysis Results:")
            st.write(analysis_feedback)

        elif action == "Job Recommendations":
            # Prepare job recommendations prompt
            recommendations_prompt = f"""
            Based on the following resume content, suggest suitable job roles or industries for the candidate. 
            Ensure the roles are appropriate to the candidate's skills, education, and experience level.
            
            Resume Content:
            {resume_text}
            """
            job_recommendations = call_groqcloud(recommendations_prompt)
            st.write("### Job Recommendations:")
            st.write(job_recommendations)

        elif action == "Job Matching":
            # Ask user for job role input
            job_role = st.text_input("Enter the job role you're interested in:")
            if job_role:
                # Prepare job matching prompt
                job_matching_prompt = f"""
                Evaluate how well the candidate's resume matches the job role "{job_role}".
                Provide a match percentage and suggest ways to improve the chances of landing this role.
                
                Resume Content:
                {resume_text}
                """
                job_match_feedback = call_groqcloud(job_matching_prompt)
                st.write("### Job Match Analysis:")
                st.write(job_match_feedback)

        # Cleanup temporary file
        os.remove(file_path)


if __name__ == "__main__":
    main()
