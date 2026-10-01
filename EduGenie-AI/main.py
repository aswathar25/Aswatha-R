import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import recommend_learning_path


load_dotenv()

app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)


# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")


# -----------------------------
# Request Models
# -----------------------------

class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1)


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1)


# -----------------------------
# Home Page
# -----------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "gemini_configured": bool(os.getenv("GEMINI_API_KEY"))
    }


# -----------------------------
# Question & Answer
# -----------------------------

@app.post("/qa")
async def qa(request: QuestionRequest):
    try:
        result = answer_question(request.question)

        return {
            "success": True,
            "result": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# -----------------------------
# Explanation
# -----------------------------

@app.post("/explain")
async def explain(request: QuestionRequest):
    try:
        result = explain_topic(request.question)

        return {
            "success": True,
            "result": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# -----------------------------
# Quiz
# -----------------------------

@app.post("/quiz")
async def quiz(request: QuestionRequest):
    try:
        result = generate_quiz(request.question)

        return {
            "success": True,
            "result": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# -----------------------------
# Summary
# -----------------------------

@app.post("/summarize")
async def summarize(request: TextRequest):
    try:
        result = summarize_text(request.text)

        return {
            "success": True,
            "result": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# -----------------------------
# Learning Recommendations
# -----------------------------

@app.post("/learn/recommendations")
async def learning_recommendations(request: QuestionRequest):
    try:
        result = recommend_learning_path(request.question)

        return {
            "success": True,
            "result": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )