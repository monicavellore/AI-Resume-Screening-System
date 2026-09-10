from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Resume Screening API")


class ResumeRequest(BaseModel):
    resume_text: str
    job_description: str


@app.get("/")
def home():
    return {
        "message": "AI Resume Screening API is running"
    }


@app.post("/analyze")
def analyze_resume(data: ResumeRequest):

    resume_words = set(data.resume_text.lower().split())
    jd_words = set(data.job_description.lower().split())

    matched_words = resume_words.intersection(jd_words)

    if len(jd_words) > 0:
        match_score = round(
            (len(matched_words) / len(jd_words)) * 100, 2
        )
    else:
        match_score = 0

    return {
        "match_score": match_score,
        "matched_terms": sorted(list(matched_words)),
        "message": "Resume analyzed successfully"
    }