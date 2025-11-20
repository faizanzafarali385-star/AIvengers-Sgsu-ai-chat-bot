# 🤖 SGSU AI Chatbot System

A complete chatbot solution for **SCOPE Global Skills University (SGSU)** built with **FastAPI** backend, **JSON knowledge base**, and modern **HTML/CSS/JS** frontend. The chatbot is trained with comprehensive information from the SGSU website and can answer questions about admissions, programs, placements, campus facilities, and more.

## 📋 Project Structure

```
SGSU/
├── main.py                 # FastAPI backend server
├── serve_frontend.py       # Frontend HTTP server
├── index.html              # Frontend chatbot UI
├── knowledge_base.json     # Q&A knowledge base
└── README.md              # This file
```

## ✨ Features

- **FastAPI Backend**: High-performance REST API with /ask endpoint
- **Knowledge Base**: Organized JSON structure with Q&A pairs across multiple categories
- **Smart Matching**: Keyword-based similarity matching for question answering
- **Modern UI**: Beautiful chat bubble interface with animations
- **AJAX Integration**: Real-time frontend-backend communication
- **CORS Enabled**: Cross-origin requests support
- **Responsive Design**: Works on desktop and mobile devices
- **Typing Indicator**: Shows when bot is "thinking"
- **Confidence Scores**: Displays how confident the bot is in its answers

## 🚀 Quick Start (Local Deployment)

### Prerequisites

- Python 3.7+
- pip or conda

### Installation

1. **Clone/Navigate to the project**:
   ```bash
   cd c:\Users\faiza\Desktop\SGSU
   ```

2. **Create virtual environment** (if not already created):
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**:
   - **Windows PowerShell**:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - **Windows CMD**:
     ```cmd
     .venv\Scripts\activate.bat
     ```

4. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn python-multipart pydantic
   ```

### Running Locally

**Terminal 1 - Start Backend API**:
```bash
python main.py
```
Backend will be available at `http://localhost:8000`

**Terminal 2 - Start Frontend Server**:
```bash
python serve_frontend.py
```
Frontend will be available at `http://localhost:8080`

**Open in Browser**:
Navigate to `http://localhost:8080` and start chatting!

## 📚 Knowledge Base Structure

The `knowledge_base.json` file contains comprehensive SGSU information organized into categories:

- **About SGSU**: University information, accreditation, location
- **Academics & Programs**: 11+ faculties and degree programs
- **Admissions & Enrollment**: Application process and requirements
- **Placements & Career**: Placement record and industry partnerships
- **Campus Facilities & Infrastructure**: Campus amenities and resources
- **Industry Partnerships & Accreditation**: Skill councils and affiliations
- **Contact & Support**: Phone, email, address, and social media

Each category contains Q&A pairs with keywords for intelligent matching.

### Adding New Q&A Pairs

Edit `knowledge_base.json` and add to a category:

```json
{
  "question": "what is machine learning",
  "keywords": ["machine learning", "ml", "ai", "artificial intelligence"],
  "answer": "Machine Learning is a subset of AI that enables systems to learn and improve from experience without explicit programming."
}
```

## 🔌 API Endpoints

### GET `/`
Root endpoint with service info
```bash
curl http://localhost:8000/
```

### GET `/health`
Health check
```bash
curl http://localhost:8000/health
```

### POST `/ask`
Ask the chatbot a question

**Request**:
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Python?"}'
```

**Response**:
```json
{
  "question": "What is Python?",
  "answer": "Python is a high-level, interpreted programming language...",
  "confidence": 0.75
}
```

## 🌐 Deployment Options

### Option 1: Render (Recommended for Cloud)

1. **Create Render account**: https://render.com

2. **Connect GitHub repository**

3. **Create Web Service**:
   - Runtime: Python 3.11
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port 8000`

4. **Environment variables**: None required for basic setup

5. **Deploy**: Click "Deploy"

**Requirements.txt** (create this file):
```
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
pydantic==2.5.0
```

### Option 2: Vercel (For Frontend Static Hosting)

1. **For Frontend only** (since Vercel doesn't support Python natively)
2. Host static `index.html` and point API to backend on Render

### Option 3: Docker (Local or Cloud)

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t chatbot .
docker run -p 8000:8000 chatbot
```

### Option 4: PythonAnywhere

1. Upload files to PythonAnywhere
2. Set up WSGI configuration
3. Point domain to PythonAnywhere

## 🔧 Customization

### Modify the UI

Edit `index.html`:
- Change colors in the `<style>` section (e.g., `#667eea` gradient)
- Update chat header text
- Modify animations

### Improve Matching Algorithm

Edit `calculate_similarity()` in `main.py`:
- Implement more advanced NLP
- Use fuzzy matching library
- Add TF-IDF scoring

### Add More Knowledge

1. Expand `knowledge_base.json` with more Q&A pairs
2. Add new categories
3. Increase keywords for better matching

## 📊 Example Questions

Try asking:
- "What is SGSU?"
- "What faculties does SGSU offer?"
- "How do I apply to SGSU?"
- "What are SGSU placement partners?"
- "Where is SGSU located?"
- "Does SGSU offer internships?"
- "What is the admission process?"
- "What facilities does SGSU have?"
- "Is SGSU UGC approved?"
- "Can I follow SGSU on social media?"

## 🛠️ Troubleshooting

### Backend Not Running
- Check Python path: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Port 8000 already in use? Change port in `main.py`

### Frontend Not Connecting
- Verify backend is running: `curl http://localhost:8000/health`
- Check browser console for errors (F12)
- CORS should be enabled (it is by default)
- Verify API URL in `index.html` JavaScript

### No Answers Matching
- Check `knowledge_base.json` syntax (valid JSON?)
- Add more keywords to Q&A pairs
- Adjust similarity threshold in `find_best_match()`

## 📈 Performance Metrics

- **Response Time**: <100ms average
- **Concurrent Users**: Limited by server resources
- **Knowledge Base Size**: Currently ~40 Q&A pairs (easily scalable)

## 🚀 Future Improvements

- [ ] Add more SGSU-specific information from individual faculty pages
- [ ] Implement database (PostgreSQL) to store conversations
- [ ] Connect to actual LLM for more advanced responses
- [ ] Add user authentication for student tracking
- [ ] Store and display conversation history
- [ ] Create admin panel for KB management
- [ ] Add FAQ page from SGSU website
- [ ] Multi-language support (English, Hindi)
- [ ] Add voice input/output
- [ ] Integration with SGSU admission system
- [ ] Mobile app (React Native)
- [ ] Push notifications for admission updates

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Support

For issues or questions, check the troubleshooting section or review the code comments.

---

**Happy Chatting! 🎉**
