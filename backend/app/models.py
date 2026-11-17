"""Pydantic schemas for request and response validation."""
from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    """Incoming user question schema."""
    question: str = Field(..., min_length=1, description="Question asked by the user")


class AnswerResponse(BaseModel):
    """Outgoing chatbot answer schema."""
    question: str
    answer: str
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
