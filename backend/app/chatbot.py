"""Core Chatbot logic, knowledge base matching, and OpenRouter integration."""
import json
import random
import re
import requests
from typing import Tuple, Optional, Dict, Any, Set

from backend.app.config import (
    KNOWLEDGE_BASE_PATH,
    OPENROUTER_API_KEYS,
    OPENROUTER_API_URL,
    USE_OPENROUTER
)

# Counter for rotating between OpenRouter API keys
API_KEY_COUNTER = 0

STOP_WORDS = {
    'what', 'is', 'are', 'the', 'tell', 'me', 'about', 'how', 'do', 'i', 
    'to', 'at', 'in', 'for', 'of', 'a', 'an', 'can', 'you', 'please', 
    'give', 'some', 'there', 'any', 'my', 'we', 'your', 'and', 'or', 'on', 
    'with', 'from', 'all', 'would', 'like', 'know', 'information', 'details', 'show'
}

GENERIC_WORDS = {'sgsu', 'university', 'college', 'campus', 'student', 'institute', 'institution', 'available'}


def load_knowledge_base() -> Dict[str, Any]:
    """Load the knowledge base from JSON file."""
    try:
        with open(KNOWLEDGE_BASE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"Knowledge base file not found at: {KNOWLEDGE_BASE_PATH}")


# Initialize knowledge base in memory
knowledge_base = load_knowledge_base()


def normalize_text(text: str) -> str:
    """Normalize text by lowercasing, handling common acronyms, and stripping punctuation."""
    text = text.lower().strip()
    text = re.sub(r'b\.?tech', 'btech', text)
    text = re.sub(r'm\.?tech', 'mtech', text)
    text = re.sub(r'b\.?sc', 'bsc', text)
    text = re.sub(r'm\.?sc', 'msc', text)
    text = re.sub(r'b\.?com', 'bcom', text)
    text = re.sub(r'm\.?com', 'mcom', text)
    text = re.sub(r'b\.?ba', 'bba', text)
    text = re.sub(r'm\.?ba', 'mba', text)
    text = re.sub(r'b\.?ca', 'bca', text)
    text = re.sub(r'm\.?ca', 'mca', text)
    text = re.sub(r'b\.?ed', 'bed', text)
    text = re.sub(r'wi-?fi', 'wifi', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    return ' '.join(text.split())


def stem_word(word: str) -> str:
    """Basic English stemming for common suffixes to handle plurals/forms."""
    if word.endswith('ies') and len(word) > 4:
        return word[:-3] + 'y'
    if word.endswith('es') and len(word) > 3:
        return word[:-2]
    if word.endswith('s') and not word.endswith('ss') and len(word) > 2:
        return word[:-1]
    if word.endswith('ing') and len(word) > 4:
        return word[:-3]
    return word


def extract_content_words(text: str) -> Set[str]:
    """Extract stemmed content words excluding stop words."""
    words = normalize_text(text).split()
    return {stem_word(w) for w in words if w not in STOP_WORDS}


def calculate_similarity(query: str, text: str) -> float:
    """Calculate semantic similarity between query and target text."""
    query_norm = normalize_text(query)
    text_norm = normalize_text(text)
    
    if not query_norm or not text_norm:
        return 0.0

    if query_norm == text_norm:
        return 1.0

    if query_norm in text_norm or text_norm in query_norm:
        return 0.90

    q_content = extract_content_words(query)
    t_content = extract_content_words(text)

    if not q_content or not t_content:
        return 0.0

    inter = q_content & t_content
    union = q_content | t_content

    if not inter:
        return 0.0

    jaccard = len(inter) / len(union)
    precision = len(inter) / len(q_content)
    score = (jaccard * 0.4) + (precision * 0.6)

    specific_inter = {w for w in inter if w not in GENERIC_WORDS}
    if specific_inter:
        score += 0.15 * min(len(specific_inter), 2)

    return min(score, 1.0)


def score_qa_pair(query_norm: str, query_content: Set[str], qa: Dict[str, Any]) -> float:
    """Score how well a QA pair answers the user query."""
    best_score = 0.0
    q_text = normalize_text(qa['question'])
    q_content = extract_content_words(qa['question'])

    # 1. Direct question match
    if query_norm == q_text:
        return 1.0

    if query_norm in q_text or q_text in query_norm:
        best_score = max(best_score, 0.90)

    # 2. Content word overlap with question
    if query_content and q_content:
        inter = query_content & q_content
        union = query_content | q_content
        if inter:
            jaccard = len(inter) / len(union)
            precision = len(inter) / len(query_content)
            score = (jaccard * 0.4) + (precision * 0.6)
            specific_inter = {w for w in inter if w not in GENERIC_WORDS}
            if specific_inter:
                score += 0.15 * min(len(specific_inter), 2)
            best_score = max(best_score, score)

    # 3. Match against keywords
    padded_query = f" {query_norm} "
    for kw in qa.get('keywords', []):
        kw_norm = normalize_text(kw)
        if not kw_norm or kw_norm in STOP_WORDS:
            continue

        padded_kw = f" {kw_norm} "
        is_generic = kw_norm in GENERIC_WORDS

        # Whole-phrase or whole-word match
        if padded_kw in padded_query or query_norm == kw_norm:
            kw_words = kw_norm.split()
            if len(kw_words) >= 2:
                best_score = max(best_score, 0.96)
            elif not is_generic:
                best_score = max(best_score, 0.88)
            else:
                best_score = max(best_score, 0.45)
        elif len(kw_norm.split()) >= 2 and kw_norm in query_norm:
            best_score = max(best_score, 0.80)

        # Keyword content words overlap (whole words only)
        kw_content = extract_content_words(kw)
        if query_content and kw_content:
            inter = query_content & kw_content
            if len(inter) == len(kw_content) and len(kw_content) >= 1:
                specific_kw = {w for w in kw_content if w not in GENERIC_WORDS}
                if specific_kw:
                    match_val = 0.75 + (0.1 * min(len(specific_kw), 3))
                    best_score = max(best_score, match_val)

    return min(best_score, 1.0)


def find_best_match(question: str) -> Tuple[Optional[Dict[str, Any]], float]:
    """Find the best matching Q&A pair from the knowledge base."""
    query_norm = normalize_text(question)
    query_content = extract_content_words(question)

    best_match = None
    best_score = 0.0

    for category, category_data in knowledge_base.get("categories", {}).items():
        for qa_pair in category_data.get("qa_pairs", []):
            score = score_qa_pair(query_norm, query_content, qa_pair)
            if score > best_score:
                best_score = score
                best_match = qa_pair

    return best_match, best_score


def is_simple_greeting(question: str) -> bool:
    """Check if the question is a simple greeting."""
    question_lower = question.lower().strip()
    simple_greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'howdy', 'namaste']
    return any(re.search(rf'\b{re.escape(g)}\b', question_lower) for g in simple_greetings)


def get_greeting_response() -> str:
    """Return a natural greeting response."""
    greetings = [
        "Hi there! Welcome to SGSU Chatbot. How can I help you with information about SCOPE Global Skills University?",
        "Hello! I'm here to help with any questions about SGSU. What would you like to know?",
        "Hey! Great to meet you. Ask me anything about SGSU courses, admissions, placements, or facilities and I'll be happy to help!",
        "Good day! I'm your SGSU assistant. What would you like to know about the university?"
    ]
    return random.choice(greetings)


def is_sgsu_related(question: str) -> bool:
    """Check if the question is SGSU-related."""
    if is_simple_greeting(question):
        return True
    
    question_norm = normalize_text(question)
    q_words = set(question_norm.split())

    # If the user explicitly mentions SGSU or university
    if any(term in question_norm for term in ['sgsu', 'scope', 'skills university', 'sgsuniversity']):
        return True
        
    sgsu_keywords = {
        'admission', 'admissions', 'faculty', 'faculties', 'program', 'programs',
        'course', 'courses', 'placement', 'placements', 'contact', 'campus', 'facility',
        'facilities', 'infrastructure', 'engineering', 'management', 'bhopal',
        'hoshangabad', 'accreditation', 'ugc', 'skill', 'skills', 'training',
        'recruiting', 'recruiter', 'recruiters', 'recruits', 'recruit', 'companies',
        'aisect', 'grievance', 'anti ragging', 'ragging', 'sports', 'wifi', 'canteen',
        'apply', 'enroll', 'degree', 'degrees', 'scholarship', 'scholarships', 'internship',
        'internships', 'partnership', 'partners', 'industry', 'graduate', 'student',
        'students', 'academic', 'academics', 'application', 'fee', 'fees', 'cost',
        'hostel', 'library', 'lab', 'labs', 'btech', 'mtech', 'bca', 'mca', 'bba', 'mba',
        'bsc', 'msc', 'bcom', 'mcom', 'ba', 'ma', 'bed', 'diploma', 'exam', 'exams',
        'entrance', 'clubs', 'fest', 'fests', 'girls', 'safety', 'security', 'cpc',
        'salary', 'package', 'jobs', 'job', 'requirement', 'requirements', 'eligibility',
        'specialization', 'specializations', 'branch', 'branches', 'location', 'located',
        'address', 'where', 'syllabus', 'curriculum', 'website'
    }
    
    if q_words & sgsu_keywords:
        return True
        
    return any(kw in question_norm for kw in ['anti ragging', 'scope campus', 'skills university'])


def format_as_keypoints(text: str) -> str:
    """Format text cleanly for display."""
    lines = text.split('\n')
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            formatted_lines.append("")
            continue
        
        # Keep clean bullet points or numbers intact
        if line.startswith(('•', '-', '*', '1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
            formatted_lines.append(line)
        else:
            formatted_lines.append(line)
            
    return '\n'.join(formatted_lines).strip()


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
You are conversational, helpful, and answer accurately using this knowledge base:

KNOWLEDGE BASE:
{kb_context}

Format your answers with clear bullet points and helpful guidance."""
        
        payload = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=8
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'choices' in data and len(data['choices']) > 0:
                answer_text = data['choices'][0]['message']['content'].strip()
                return format_as_keypoints(answer_text)
        
        return None
        
    except Exception as e:
        print(f"OpenRouter API error: {e}")
        return None


def get_answer(question: str) -> Tuple[str, float]:
    """Get an answer for the user's question with KB matching and OpenRouter fallback."""
    if is_simple_greeting(question):
        return get_greeting_response(), 1.0
    
    if not is_sgsu_related(question):
        fallback_responses = knowledge_base.get("fallback_responses", [
            "I'm specifically designed to help with SCOPE Global Skills University (SGSU) queries. For questions about admissions, courses, fees, placements, or campus facilities, feel free to ask!"
        ])
        return random.choice(fallback_responses), 0.0
    
    # Try OpenRouter API if enabled and keys exist
    if USE_OPENROUTER and OPENROUTER_API_KEYS:
        try:
            answer = get_answer_from_openrouter(question)
            if answer:
                return answer, 0.95
        except Exception:
            pass
    
    # Accurate Knowledge Base match
    match, confidence = find_best_match(question)
    
    if match and confidence >= 0.35:
        return match["answer"], round(confidence, 2)
    else:
        fallback_responses = knowledge_base.get("fallback_responses", [
            "I'm not completely certain about that specific query. Please contact the SGSU Admissions Desk at +91-7552432903/904 or visit https://sgsuniversity.ac.in/ for verified details."
        ])
        return random.choice(fallback_responses), 0.0
