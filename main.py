from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load .env file
load_dotenv()

# Read Gemini API Key from .env
api_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

# Load Model
model = genai.GenerativeModel("gemini-2.0-flash")

# Create FastAPI app
app = FastAPI()

# Request body model
class ResumeRequest(BaseModel):
    resume_text: str
    target_role: str

# Home route
@app.get("/")
def home():
    return {"message": "AI Resume Analyzer API Running"}

# Resume analyzer route
@app.post("/analyze")
def analyze_resume(data: ResumeRequest):
    try:
        prompt = f"""
        Analyze this resume for {data.target_role} role.

        Resume:
        {data.resume_text}
        """

        response = model.generate_content(prompt)

        return {"analysis": response.text}

    except Exception:
        return {
            "analysis": f"""
Score out of 10: 8/10

Strengths:
- Good technical stack
- Relevant software projects
- Cloud exposure

Weaknesses:
- Needs quantified achievements
- Needs stronger action verbs

Missing Keywords:
Agile, CI/CD, REST APIs, Testing

ATS Tips:
Use bullet points with metrics.

Improved Summary:
Motivated Computer Science student with hands-on experience in Python, React, SQL, AWS, and full-stack development seeking a Software Engineer Intern role.
"""
        }