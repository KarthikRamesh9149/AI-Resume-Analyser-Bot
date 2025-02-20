# AI Resume Analyser Bot  

The **AI Resume Analyser Bot** is an intelligent tool that analyzes resumes, provides detailed feedback, and recommends suitable job roles based on the candidate's skills, education, and experience. It leverages **LLMs (GroqCloud API), text extraction, and NLP-based analysis** to offer insights into resume quality, job fit, and areas for improvement.  

This bot enables users to upload a **PDF resume**, extract its content, and receive AI-generated **resume analysis, job recommendations, and job matching scores**. With **automated text processing and structured evaluation**, it provides valuable career insights for job seekers and professionals.  

---

## Features  

- **Resume Text Extraction** – Uses `PyPDF2` to extract text from uploaded PDF resumes.  
- **AI-Powered Resume Analysis** – Evaluates key resume sections, including **skills, experience, education, and certifications**.  
- **Job Recommendations** – Suggests suitable job roles based on the candidate's background.  
- **Job Matching Score** – Compares resumes to desired job roles and provides a match percentage with improvement suggestions.  
- **GroqCloud LLM Integration** – Utilizes the `Mixtral-8x7B-32768` model for **advanced NLP-based analysis and job matching**.  
- **Streamlit-Based UI** – Offers an interactive web interface for resume uploads and analysis.  

---

## Tech Stack  

- **Programming Language:** Python  
- **Framework:** Streamlit  
- **LLM API:** GroqCloud (`Mixtral-8x7B-32768`)  
- **Text Extraction:** PyPDF2  
- **Text Splitting:** LangChain CharacterTextSplitter  
- **Environment Management:** Python `dotenv` for API key handling  
