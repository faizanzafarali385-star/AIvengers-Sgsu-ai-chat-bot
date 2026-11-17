"""Core Chatbot logic, knowledge base matching, and OpenRouter integration."""
import json
import random
import requests
from typing import Tuple, Optional, Dict, Any

from backend.app.config import (
    KNOWLEDGE_BASE_PATH,
    OPENROUTER_API_KEYS,
    OPENROUTER_API_URL,
    USE_OPENROUTER
)

# Counter for rotating between OpenRouter API keys
API_KEY_COUNTER = 0


def load_knowledge_base() -> Dict[str, Any]:
    """Load the knowledge base from JSON file."""
    try:
        with open(KNOWLEDGE_BASE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"Knowledge base file not found at: {KNOWLEDGE_BASE_PATH}")


# Initialize knowledge base in memory
knowledge_base = load_knowledge_base()


def calculate_similarity(query: str, text: str) -> float:
    """Calculate similarity between query and text using Jaccard word similarity."""
    query_words = set(query.lower().split())
    text_words = set(text.lower().split())
    
    if not query_words or not text_words:
        return 0.0
    
    intersection = len(query_words & text_words)
    union = len(query_words | text_words)
    
    return intersection / union if union > 0 else 0.0


def find_best_match(question: str) -> Tuple[Optional[Dict[str, Any]], float]:
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
            
            # Best score between question and keywords
            current_score = max(question_score, max_keyword_score)
            
            if current_score > best_score:
                best_score = current_score
                best_match = qa_pair
    
    return best_match, best_score


def is_simple_greeting(question: str) -> bool:
    """Check if the question is a simple greeting."""
    question_lower = question.lower().strip()
    simple_greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'howdy']
    return any(greeting in question_lower for greeting in simple_greetings)


def get_greeting_response() -> str:
    """Return a natural greeting response."""
    greetings = [
        "Hi there! Welcome to SGSU Chatbot. How can I help you with information about SCOPE Global Skills University?",
        "Hello! I'm here to help with any questions about SGSU. What would you like to know?",
        "Hey! Great to meet you. Ask me anything about SGSU and I'll be happy to help!",
        "Good day! I'm your SGSU assistant. What would you like to know about the university?"
    ]
    return random.choice(greetings)


def is_sgsu_related(question: str) -> bool:
    """Check if the question is SGSU-related."""
    question_lower = question.lower().strip()
    
    if is_simple_greeting(question):
        return True
    
    sgsu_keywords = [
        'sgsu', 'scope global skills university', 'admission', 'faculty', 'program', 
        'course', 'placement', 'contact', 'campus', 'facility', 'infrastructure',
        'engineering', 'management', 'future skills', 'bhopal', 'hoshangabad',
        'accreditation', 'ugc', 'skill', 'training', 'recruiting', 'recruiter',
        'aisect', 'grievance', 'anti ragging', 'sports', 'wifi', 'canteen',
        'sgsuniversity', 'apply', 'enroll', 'degree', 'scholarship', 'internship',
        'partnership', 'industry', 'graduate', 'student', 'academic', 'application'
    ]
    
    return any(keyword in question_lower for keyword in sgsu_keywords)


def format_as_keypoints(text: str) -> str:
    """Format text as key points with bullet points and line breaks."""
    lines = text.split('\n')
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        line = line.lstrip('•-*·').strip()
        
        if line and not line.startswith('•'):
            formatted_lines.append(f"• {line}")
            formatted_lines.append("")
        elif line.startswith('•'):
            formatted_lines.append(line)
            formatted_lines.append("")
    
    while formatted_lines and formatted_lines[-1] == "":
        formatted_lines.pop()
    
    return '\n'.join(formatted_lines)


def build_kb_context() -> str:
    """Build a text context from the knowledge base for the LLM."""
    context = ""
    for category, category_data in knowledge_base.get("categories", {}).items():
        context += f"\n{category}:\n"
        for qa_pair in category_data.get("qa_pairs", []):
            context += f"- Q: {qa_pair['question']}\n  A: {qa_pair['answer']}\n"
    return context


def get_answer_from_openrouter(question: str) -> Optional[str]:
    """Query OpenRouter API for intelligent response using advanced LLM with key rotation."""
    global API_KEY_COUNTER
    
    if not OPENROUTER_API_KEYS:
        return None

    try:
        current_key = OPENROUTER_API_KEYS[API_KEY_COUNTER % len(OPENROUTER_API_KEYS)]
        API_KEY_COUNTER += 1
        
        headers = {
            "Authorization": f"Bearer {current_key}",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "SGSU Chatbot",
            "Content-Type": "application/json"
        }
        
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
                return format_as_keypoints(answer_text)
        
        return None
        
    except Exception as e:
        print(f"Error calling OpenRouter API: {e}")
        return None


def get_answer(question: str) -> Tuple[str, float]:
    """Get an answer for the user's question using OpenRouter API with KB fallback."""
    if is_simple_greeting(question):
        return get_greeting_response(), 1.0
    
    if not is_sgsu_related(question):
        fallback_responses = knowledge_base.get("fallback_responses", [
            "I'm not sure about that specific question. For detailed information, please contact SGSU at info@sgsuniversity.ac.in or visit https://sgsuniversity.ac.in/"
        ])
        return random.choice(fallback_responses), 0.0
    
    # Try OpenRouter API first
    if USE_OPENROUTER and OPENROUTER_API_KEYS:
        try:
            answer = get_answer_from_openrouter(question)
            if answer:
                return answer, 0.95
        except Exception as e:
            print(f"OpenRouter API error: {e}")
    
    # Fall back to local knowledge base
    match, confidence = find_best_match(question)
    
    if match and confidence > 0.2:
        return match["answer"], confidence
    else:
        fallback_responses = knowledge_base.get("fallback_responses", [
            "I'm not sure about that. Could you ask something else?"
        ])
        return random.choice(fallback_responses), 0.0
