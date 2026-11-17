"""FastAPI application definition and route handlers."""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.config import FRONTEND_DIR
from backend.app.models import QuestionRequest, AnswerResponse
from backend.app.chatbot import get_answer

# Initialize FastAPI app
app = FastAPI(
    title="SGSU Chatbot API",
    description="Official API for SCOPE Global Skills University AI Chatbot",
    version="2.0.0"
)

# CORS middleware to allow requests from any frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "chatbot-api"}


@app.get("/api")
@app.get("/api/health")
async def api_info():
    """API information endpoint."""
    return {
        "service": "SGSU Chatbot API",
        "status": "healthy",
        "version": "2.0.0",
        "endpoints": {
            "ask": "POST /ask",
            "health": "GET /health"
        }
    }


@app.post("/ask", response_model=AnswerResponse)
@app.post("/api/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Main endpoint to ask questions to the chatbot.
    
    Args:
        request: QuestionRequest containing the user's question
    
    Returns:
        AnswerResponse with the answer and confidence score
    """
    if not request.question or not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        answer, confidence = get_answer(request.question)
        return AnswerResponse(
            question=request.question,
            answer=answer,
            confidence=confidence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Mount the frontend static files so opening http://localhost:8000 displays the UI directly
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
else:
    @app.get("/")
    async def root_fallback():
        return {
            "message": "SGSU Chatbot API is running",
            "version": "2.0.0",
            "note": "Frontend directory not found. Please verify the project structure."
        }
