from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import random
import re
from pathlib import Path
import requests
import os

# Initialize FastAPI app
app = FastAPI(title="Chatbot API", version="1.0.0")

# OpenRouter API Configuration - Dual API Keys for better load distribution
OPENROUTER_API_KEYS = [
    "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",
    "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"
]
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
USE_OPENROUTER = True  # Set to False to use only local KB
API_KEY_COUNTER = 0  # Counter for rotating between API keys

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    question: str
    answer: str
    confidence: float

# Load knowledge base
def load_knowledge_base():
    """Load the knowledge base from JSON file."""
    kb_path = Path(__file__).parent / "knowledge_base.json"
    try:
        with open(kb_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise Exception("Knowledge base file not found!")

# Initialize knowledge base
knowledge_base = load_knowledge_base()

def calculate_similarity(query, text):
    """Calculate similarity between query and text using simple keyword matching."""
    query_words = set(query.lower().split())
    text_words = set(text.lower().split())
    
    # Simple Jaccard similarity
    if not query_words or not text_words:
        return 0.0
    
    intersection = len(query_words & text_words)
    union = len(query_words | text_words)
    
    return intersection / union

def find_best_match(question):
    """Find the best matching Q&A pair from the knowledge base."""
    question_lower = question.lower().strip()
    best_match = None
    best_score = 0.0
    
    # Search through all categories
    for category, category_data in knowledge_base.get("categories", {}).items():
        for qa_pair in category_data.get("qa_pairs", []):
            # Check direct question match
            question_score = calculate_similarity(
                question_lower,
                qa_pair["question"].lower()
            )
            
            # Check keywords match
            keywords = qa_pair.get("keywords", [])
            keyword_scores = [
                calculate_similarity(question_lower, keyword)
                for keyword in keywords
            ]
            
            max_keyword_score = max(keyword_scores) if keyword_scores else 0.0
            
            # Use the best score between question and keywords
            current_score = max(question_score, max_keyword_score)
            
            if current_score > best_score:
                best_score = current_score
                best_match = qa_pair
    
    return best_match, best_score

def is_simple_greeting(question):
    """Check if the question is a simple greeting."""
    question_lower = question.lower().strip()
    simple_greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'howdy']
    return any(greeting in question_lower for greeting in simple_greetings)

def get_greeting_response():
    """Return a natural greeting response."""
    greetings = [
        "Hi there! Welcome to SGSU Chatbot. How can I help you with information about SCOPE Global Skills University?",
        "Hello! I'm here to help with any questions about SGSU. What would you like to know?",
        "Hey! Great to meet you. Ask me anything about SGSU and I'll be happy to help!",
        "Good day! I'm your SGSU assistant. What would you like to know about the university?"
    ]
    return random.choice(greetings)

def is_sgsu_related(question):
    """Check if the question is SGSU-related."""
    question_lower = question.lower().strip()
    
    # Check if it's a simple greeting first
    if is_simple_greeting(question):
        return True
    
    # List of SGSU-related keywords
    sgsu_keywords = [
        'sgsu', 'scope global skills university', 'admission', 'faculty', 'program', 
        'course', 'placement', 'contact', 'campus', 'facility', 'infrastructure',
        'engineering', 'management', 'future skills', 'bhopal', 'hoshangabad',
        'accreditation', 'ugc', 'skill', 'training', 'recruiting', 'recruiter',
        'aisect', 'grievance', 'anti ragging', 'sports', 'wifi', 'canteen',
        'sgsuniversity', 'apply', 'enroll', 'degree', 'scholarship', 'internship',
        'partnership', 'industry', 'graduate', 'student', 'academic', 'application'
    ]
    
    # Check if any SGSU keyword is in the question
    for keyword in sgsu_keywords:
        if keyword in question_lower:
            return True
    
    return False

def get_answer(question):
    """Get an answer for the user's question using OpenRouter API with KB fallback."""
    
    # Check if it's a simple greeting
    if is_simple_greeting(question):
        return get_greeting_response(), 1.0
    
    # Check if question is SGSU-related
    if not is_sgsu_related(question):
        # Return fallback response for non-SGSU questions
        fallback_responses = knowledge_base.get("fallback_responses", [
            "I'm not sure about that specific question. For detailed information, please contact SGSU at info@sgsuniversity.ac.in or visit https://sgsuniversity.ac.in/"
        ])
        return random.choice(fallback_responses), 0.0
    
    # Try OpenRouter API first for SGSU questions with dual key support
    if USE_OPENROUTER and OPENROUTER_API_KEYS:
        try:
            answer = get_answer_from_openrouter(question)
            if answer:
                return answer, 0.95  # High confidence for LLM responses
        except Exception as e:
            print(f"OpenRouter API error: {e}")
            # Fall back to local KB
    
    # Fall back to local knowledge base
    match, confidence = find_best_match(question)
    
    if match and confidence > 0.2:  # Threshold for accepting a match
        return match["answer"], confidence
    else:
        # Return a random fallback response
        fallback_responses = knowledge_base.get("fallback_responses", [
            "I'm not sure about that. Could you ask something else?"
        ])
        return random.choice(fallback_responses), 0.0

def get_answer_from_openrouter(question):
    """Query OpenRouter API for intelligent response using advanced LLM with dual key rotation."""
    global API_KEY_COUNTER
    
    try:
        # Rotate through available API keys for better load distribution
        current_key = OPENROUTER_API_KEYS[API_KEY_COUNTER % len(OPENROUTER_API_KEYS)]
        API_KEY_COUNTER += 1
        
        headers = {
            "Authorization": f"Bearer {current_key}",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "SGSU Chatbot",
            "Content-Type": "application/json"
        }
        
        # Build context from knowledge base for better responses
        kb_context = build_kb_context()
        
        system_prompt = f"""You are an intelligent AI assistant for SCOPE Global Skills University (SGSU). 
You are conversational, helpful, and excellent at understanding user intent even with informal language, typos, or casual phrasing.

KNOWLEDGE BASE:
{kb_context}

BEHAVIORAL GUIDELINES:

1. UNDERSTAND CONTEXT & INTENT:
   - Understand synonyms (e.g., "course" = "program", "fee" = "cost", "teachers" = "faculty")
   - Understand casual variations (e.g., "how do I get in" = "admission", "where r u from" = "location")
   - Understand abbreviations (e.g., "UG" = "undergraduate", "PG" = "postgraduate")
   - Handle typos and spelling mistakes gracefully
   - Infer meaning from incomplete sentences

2. SGSU-RELATED QUESTIONS - Answer helpfully:
   - Use the knowledge base to provide accurate information
   - Format as key points with bullet points (•) - each on separate line
   - Be conversational and friendly, not robotic
   - If info is incomplete, suggest how to get more details
   - Make connections to related info the user might find helpful

3. GREETINGS & CASUAL CHAT:
   - Respond naturally to "hi", "hello", "hey", "how are you", etc.
   - Keep greetings warm and brief (1-2 sentences)
   - Then smoothly transition to offering SGSU help
   - Example: "Hey! I'm doing great, thanks for asking! How can I help you with info about SGSU?"

4. NON-SGSU QUESTIONS - FIRMLY REDIRECT:
   - For unrelated questions like "what is a dog", "tell me a joke", "how to cook", etc.
   - Use one of these fallback responses:
     * "I'm not sure about that specific question. For detailed information, please contact SGSU at info@sgsuniversity.ac.in or visit https://sgsuniversity.ac.in/"
     * "That's a great question! I don't have that specific information in my knowledge base. Please reach out to the admissions team at +91-7552432903/904."
     * "I don't have that information yet. Please visit the SGSU website or contact the university directly for the most accurate and up-to-date information."
     * "I'm specifically designed to help with SGSU-related questions. Feel free to ask me anything about the university!"

5. TONE & PERSONALITY:
   - Be conversational and approachable
   - Use "I" and "we" to sound natural
   - Show enthusiasm about SGSU
   - Be concise but informative
   - Avoid being robotic or overly formal

6. KEY POINT FORMAT (for SGSU answers):
   • Main information here
   • Supporting detail or next step
   • Additional relevant information

Remember: You understand natural language, slang, abbreviations, and user intent. Always try to be helpful!"""
        
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            "temperature": 0.75,
            "max_tokens": 600,
            "top_p": 0.9
        }
        
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                answer_text = data['choices'][0]['message']['content'].strip()
                # Ensure bullet points are properly formatted
                formatted_answer = format_as_keypoints(answer_text)
                return formatted_answer
        
        return None
        
    except Exception as e:
        print(f"Error calling OpenRouter API: {e}")
        return None

def format_as_keypoints(text):
    """Format text as key points with bullet points and line breaks."""
    lines = text.split('\n')
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Remove existing bullet points or dashes
        line = line.lstrip('•-*·').strip()
        
        # Add bullet point if not already present
        if line and not line.startswith('•'):
            formatted_lines.append(f"• {line}")
            formatted_lines.append("")  # Add empty line for paragraph break
        elif line.startswith('•'):
            formatted_lines.append(line)
            formatted_lines.append("")  # Add empty line for paragraph break
    
    # Remove trailing empty lines
    while formatted_lines and formatted_lines[-1] == "":
        formatted_lines.pop()
    
    return '\n'.join(formatted_lines)

def build_kb_context():
    """Build a text context from the knowledge base for the LLM."""
    context = ""
    for category, category_data in knowledge_base.get("categories", {}).items():
        context += f"\n{category}:\n"
        for qa_pair in category_data.get("qa_pairs", []):
            context += f"- Q: {qa_pair['question']}\n  A: {qa_pair['answer']}\n"
    return context

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Chatbot API is running",
        "version": "1.0.0",
        "endpoints": {
            "ask": "POST /ask - Ask a question to the chatbot",
            "health": "GET /health - Check API health"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "chatbot-api"}

@app.post("/ask", response_model=AnswerResponse)
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
