# 🎓 SGSU AI Chatbot System

A complete chatbot solution for **SCOPE Global Skills University (SGSU)** built with a modular **FastAPI** backend, **JSON knowledge base** with **OpenRouter LLM fallback**, and a modern, responsive **Frontend UI** with dark mode support.

---

## 📁 Project Structure

The project has been organized into clean, modular directories:

```
SGSU/
├── backend/
│   ├── app/
│   │   ├── __init__.py           # Package marker
│   │   ├── api.py                # FastAPI app, route handlers, static file mounting
│   │   ├── chatbot.py            # Matching algorithms, prompt context & OpenRouter integration
│   │   ├── config.py             # App paths, server ports, and API key settings
│   │   └── models.py             # Pydantic schemas (QuestionRequest, AnswerResponse)
│   ├── data/
│   │   └── knowledge_base.json   # 29 SGSU Q&A pairs categorized with smart keywords
│   └── __init__.py
├── frontend/
│   ├── index.html                # Semantic chat interface
│   ├── css/
│   │   └── style.css             # UI styling, responsive design & dark mode
│   └── js/
│       └── app.js                # Chat controller, auto API detection & retry logic
├── docs/                         # Comprehensive project documentation & deployment guides
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
├── .gitignore                    # Python, VSCode, OS & build ignore rules
├── Dockerfile                    # Containerization build recipe
├── docker-compose.yml            # Multi-service container orchestration
├── main.py                       # Single-command application entrypoint
├── requirements.txt              # Python package dependencies
├── serve_frontend.py             # Optional standalone frontend server
└── README.md                     # Project overview and instructions
```

---

## ✨ Features

- **All-in-One Serving**: Starting `main.py` serves both the backend API and frontend chat interface seamlessly on `http://localhost:8000`.
- **Hybrid AI Engine**:
  - Matches user queries against verified SGSU knowledge base data using Jaccard keyword similarity.
  - Automatically queries OpenRouter (GPT) with full SGSU context for natural conversational responses.
- **Modern UI**:
  - Light / Dark mode toggle with preference persistence.
  - Interactive quick-query suggestion buttons.
  - Typing animation indicator.
  - Confidence scoring indicator.
  - Fully mobile-responsive layout.
- **Container Ready**: Ready for Docker and `docker-compose` deployments.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+ (Tested on Python 3.11 & 3.12)
- Virtual environment (recommended)

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Chatbot

#### Option A: Unified Server (Recommended - 1 Command)
```bash
python main.py
```
- Open **[http://localhost:8000](http://localhost:8000)** in your browser.
- Both the frontend UI and the REST API run simultaneously from this single server!

#### Option B: Separate Frontend & Backend Servers
- **Terminal 1 (Backend)**:
  ```bash
  python main.py
  ```
  API runs on `http://localhost:8000`

- **Terminal 2 (Frontend)**:
  ```bash
  python serve_frontend.py
  ```
  UI runs on `http://localhost:8080` (auto-connects to backend on port 8000).

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the web frontend UI |
| `GET` | `/health` | Health check endpoint returning API status |
| `POST` | `/ask` | Ask a question (`{"question": "What is SGSU?"}`) |
| `GET` | `/docs` | Interactive Swagger API documentation |

---

## 🐳 Docker Deployment

To run with Docker:
```bash
docker build -t sgsu-chatbot .
docker run -p 8000:8000 sgsu-chatbot
```

Or using Docker Compose:
```bash
docker-compose up --build
```

---

## 📚 Documentation

Detailed guides and references have been neatly filed inside the [`docs/`](file:///c:/Users/faiza/OneDrive/Desktop/SGSU%20Projects/SGSU/docs) directory:
- [docs/QUICK_START.md](file:///c:/Users/faiza/OneDrive/Desktop/SGSU%20Projects/SGSU/docs/QUICK_START.md) — Fast local deployment instructions.
- [docs/SYSTEM_OVERVIEW.md](file:///c:/Users/faiza/OneDrive/Desktop/SGSU%20Projects/SGSU/docs/SYSTEM_OVERVIEW.md) — Technical architecture overview.
- [docs/DEPLOY_RENDER.md](file:///c:/Users/faiza/OneDrive/Desktop/SGSU%20Projects/SGSU/docs/DEPLOY_RENDER.md) — Cloud deployment guide for Render.
- [docs/00_MASTER_INDEX.md](file:///c:/Users/faiza/OneDrive/Desktop/SGSU%20Projects/SGSU/docs/00_MASTER_INDEX.md) — Delivery and verification index.
