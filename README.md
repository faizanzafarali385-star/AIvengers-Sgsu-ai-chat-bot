# 🎓 SGSU AI Chatbot System

A complete, production-ready AI Chatbot solution for **SCOPE Global Skills University (SGSU)**. Built with a modular **FastAPI** backend, high-precision **NLP Knowledge Base matcher** with **OpenRouter LLM fallback**, and a modern, responsive **Frontend UI** with live dark mode and formatted markdown responses.

---

## 📁 Project Structure

The project is organized into clean, modular files and directories:

```text
SGSU/
├── backend/
│   ├── app/
│   │   ├── __init__.py           # Python package marker
│   │   ├── api.py                # FastAPI routes, health check & static UI mounting
│   │   ├── chatbot.py            # NLP matcher, intent detection & OpenRouter integration
│   │   ├── config.py             # Server host/ports, directory paths, and API keys
│   │   └── models.py             # Pydantic schemas (QuestionRequest, AnswerResponse)
│   ├── data/
│   │   └── knowledge_base.json   # 70+ SGSU Q&A pairs categorized with smart keywords
│   └── __init__.py
├── frontend/
│   ├── index.html                # Semantic, accessible chat web interface
│   ├── css/
│   │   └── style.css             # Responsive styling, animations & dark mode theme
│   └── js/
│       └── app.js                # Chat controller, markdown parser & auto-reconnect
├── docs/                         # Guides, technical overview & deployment docs
│   ├── 00_MASTER_INDEX.md
│   ├── COMPLETE_GUIDE.md
│   ├── DEPLOYMENT_READY.md
│   ├── DEPLOY_RENDER.md
│   ├── DOCUMENTATION_INDEX.md
│   ├── FINAL_SUMMARY.md
│   ├── FINAL_VERIFICATION.md
│   ├── PROJECT_COMPLETE.md
│   ├── PROJECT_SUMMARY.md
│   ├── QUICK_START.md
│   ├── SGSU_TRAINING_UPDATE.md
│   ├── START_HERE.md
│   └── SYSTEM_OVERVIEW.md
├── .env.example                  # Environment configuration template
├── .gitignore                    # Git ignore rules (Python, npm, OS, IDE)
├── Dockerfile                    # Containerization build recipe
├── docker-compose.yml            # Multi-service container orchestration
├── index.html                    # Root redirect to frontend/index.html
├── main.py                       # Single-command application entrypoint
├── requirements.txt              # Python package dependencies
├── serve_frontend.py             # Optional standalone frontend development server
└── README.md                     # Project overview and documentation
```

---

## ✨ Features

- **All-in-One Server**: Starting `main.py` simultaneously serves both the FastAPI REST backend and the frontend chat interface at `http://localhost:8000`.
- **High-Precision NLP Engine**:
  - **Stop-word & Stemming Aware**: Filters common conversational filler words (`what`, `is`, `are`, `tell`, `me`, `about`) so queries match the core intent.
  - **Whole-Word & Phrase Matching**: Prevents substring false matches (e.g. short keywords like `'it'` no longer falsely match words like `'recruits'`).
  - **Calibrated Confidence**: Direct phrase and keyword matches score `0.85`–`1.00`, with smooth fallback to friendly guidance when queries are out of scope.
  - **OpenRouter LLM Integration**: Automatic GPT fallback with full SGSU context when external API keys are configured.
- **Modern Responsive UI**:
  - **Formatted Answers**: Markdown bold headers (`**text**`), bulleted lists (`•`), and clickable links (`https://...`) rendered cleanly with proper line spacing.
  - **8 One-Click Quick Questions**: Instant answers for About SGSU, Admissions, Programs, Placements, Fee Structure, Facilities, All Courses, and B.Tech Specializations.
  - **Dark / Light Mode**: Toggle switch with persistent user preference in `localStorage`.
  - **Typing Animation & Confidence Indicators**: Real-time feedback for a natural chat experience.
- **Production & Cloud Ready**: Fully configured for Docker, Docker Compose, Render, or independent static hosting.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+ (tested on Python 3.11 & 3.12)
- Virtual environment (recommended)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Chatbot

#### Option A: Unified Server (Recommended — 1 Command)
```bash
python main.py
```
- Open **[http://localhost:8000](http://localhost:8000)** in your browser.
- Both the web chat interface and the REST API run simultaneously from this single server.

#### Option B: Separate Frontend & Backend Servers (Optional)
If you want to run or edit the frontend independently:
- **Terminal 1 (Backend)**:
  ```bash
  python main.py
  ```
  API runs on `http://localhost:8000`

- **Terminal 2 (Frontend)**:
  ```bash
  python serve_frontend.py
  ```
  Frontend runs on `http://localhost:8080` (auto-detects and connects to backend on port 8000).

#### Option C: VS Code Live Server
Opening the project with Live Server (port 5500/5501) automatically routes requests to the backend at `http://localhost:8000`.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the web frontend UI directly |
| `GET` | `/health` | Health check endpoint returning `{"status": "healthy", "service": "chatbot-api"}` |
| `POST` | `/ask` | Ask a question (`{"question": "What are the admission requirements?"}`) |
| `GET` | `/docs` | Interactive Swagger API documentation |
| `GET` | `/redoc` | ReDoc API specification |

### Example API Request (cURL)
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d "{\"question\": \"What are the placement opportunities?\"}"
```

### Example API Response
```json
{
  "question": "What are the placement opportunities?",
  "answer": "SGSU has an excellent placement record with strong partnerships with 500+ companies. We ensure practical exposure and job readiness for all students. Most graduates secure placements through campus recruitment or internship conversions.",
  "confidence": 1.0
}
```

---

## ⚙️ Environment Variables (Optional)

Create a `.env` file in the root directory (based on `.env.example`) to customize configuration:

```env
# Server Host and Port
HOST=0.0.0.0
PORT=8000
FRONTEND_PORT=8080

# OpenRouter LLM Fallback (Optional)
USE_OPENROUTER=true
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

*Note: If no OpenRouter key is provided, the chatbot seamlessly operates using its local high-speed NLP Knowledge Base.*

---

## 🐳 Docker Deployment

### Using Docker Directly:
```bash
docker build -t sgsu-chatbot .
docker run -p 8000:8000 sgsu-chatbot
```

### Using Docker Compose:
```bash
docker-compose up --build
```

---

## 📚 Documentation & Guides

Comprehensive guides and architectural documentation are available in the [`docs/`](docs/) directory:
- [docs/QUICK_START.md](docs/QUICK_START.md) — Rapid setup guide.
- [docs/SYSTEM_OVERVIEW.md](docs/SYSTEM_OVERVIEW.md) — Technical architecture and data flow.
- [docs/DEPLOY_RENDER.md](docs/DEPLOY_RENDER.md) — Cloud deployment on Render.
- [docs/SGSU_TRAINING_UPDATE.md](docs/SGSU_TRAINING_UPDATE.md) — Knowledge base categorization and training details.
- [docs/00_MASTER_INDEX.md](docs/00_MASTER_INDEX.md) — Project verification master index.
