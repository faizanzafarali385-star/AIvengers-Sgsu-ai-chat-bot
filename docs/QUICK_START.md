# 🚀 Quick Start Guide

## Running the Chatbot (Local Development)

### Option 1: Simple Python (Recommended for Testing)

**1. Open PowerShell and navigate to the project:**
```powershell
cd c:\Users\faiza\Desktop\SGSU
```

**2. Activate virtual environment:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**3. Start Backend (Terminal 1):**
```powershell
python main.py
```
✅ Backend running at `http://localhost:8000`

**4. Start Frontend (Terminal 2):**
```powershell
python serve_frontend.py
```
✅ Frontend running at `http://localhost:8080`

**5. Open in Browser:**
- Go to `http://localhost:8080`
- Start chatting! 🎉

---

### Option 2: Docker (Production-ready)

**Prerequisites:**
- Docker Desktop installed

**1. Build and run:**
```bash
docker-compose up --build
```

**2. Open:**
- Frontend: `http://localhost:8080`
- Backend: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

---

## 📝 Testing the API

### Using PowerShell:

```powershell
$question = @{question = "What is Python?"} | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:8000/ask" `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body $question
```

### Using curl:
```bash
curl -X POST http://localhost:8000/ask ^
  -H "Content-Type: application/json" ^
  -d "{\"question\": \"What is FastAPI?\"}"
```

---

## 🎯 Example Questions to Try

1. "What is Python?"
2. "How do I start a business?"
3. "What is FastAPI?"
4. "What is the Pomodoro technique?"
5. "How can you help me?"
6. "What topics do you cover?"

---

## 📂 File Descriptions

| File | Purpose |
|------|---------|
| `main.py` | FastAPI backend with /ask endpoint |
| `index.html` | Frontend chat UI (HTML/CSS/JS) |
| `knowledge_base.json` | Q&A database organized by categories |
| `serve_frontend.py` | Simple HTTP server for frontend |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Container configuration |
| `docker-compose.yml` | Multi-container setup |
| `README.md` | Full documentation |

---

## ✅ Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 8080
- [ ] Browser shows chatbot UI
- [ ] Can send messages and receive answers
- [ ] Confidence scores displayed
- [ ] CORS working (no console errors)

---

## 🔗 Important URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:8080 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| API Redoc | http://localhost:8000/redoc |

---

## 🆘 Common Issues

| Problem | Solution |
|---------|----------|
| "Port already in use" | Change port in `main.py` or `serve_frontend.py` |
| "Backend not responding" | Check if `main.py` is running |
| "No answers from bot" | Check `knowledge_base.json` is valid JSON |
| "CORS errors" | Backend CORS is enabled by default |

---

## 🚀 Next Steps

1. **Add more Q&As** to `knowledge_base.json`
2. **Customize UI colors** in `index.html`
3. **Deploy** using Docker or Render
4. **Integrate** with real LLM (OpenAI, Hugging Face)

---

**Questions?** Check the full README.md file!
