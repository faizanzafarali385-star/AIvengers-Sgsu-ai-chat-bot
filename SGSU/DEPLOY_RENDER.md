# 🌍 Deployment Guide - Render.com

This guide shows how to deploy the chatbot to Render for free or paid hosting.

## Prerequisites

- GitHub account (free)
- Render account (free tier available)
- Git installed locally

## Step 1: Prepare Your GitHub Repository

### 1a. Initialize Git (if not already done)
```powershell
cd c:\Users\faiza\Desktop\SGSU
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### 1b. Add all files
```powershell
git add .
git commit -m "Initial chatbot deployment"
```

### 1c. Push to GitHub
```powershell
git remote add origin https://github.com/YOUR_USERNAME/chatbot.git
git branch -M main
git push -u origin main
```

## Step 2: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub (recommended)
3. Connect your GitHub account

## Step 3: Deploy Backend API

### 3a. Create New Web Service
- Click "New +" → "Web Service"
- Select your GitHub repository
- Authorization: "Connect" GitHub

### 3b. Configure Service
| Setting | Value |
|---------|-------|
| **Name** | chatbot-api |
| **Runtime** | Python 3.11 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port 8000` |
| **Instance Type** | Free (or Starter+ for better performance) |

### 3c. Environment Variables
No required environment variables needed for basic setup.

### 3d. Deploy
- Click "Create Web Service"
- Wait for deployment (2-3 minutes)
- Your backend URL: `https://chatbot-api.onrender.com`

## Step 4: Update Frontend with New Backend URL

### 4a. Edit index.html
Open `index.html` and find this line:
```javascript
const API_URL = 'http://localhost:8000';
```

Replace with:
```javascript
const API_URL = 'https://chatbot-api.onrender.com';
```

### 4b. Commit and push
```powershell
git add index.html
git commit -m "Update API URL for production"
git push
```

## Step 5: Deploy Frontend (Static Site)

### Option A: Deploy as Static Site on Render

1. Click "New +" → "Static Site"
2. Select your GitHub repository
3. Configure:
   | Setting | Value |
   |---------|-------|
   | **Name** | chatbot-ui |
   | **Root Directory** | . (leave empty) |
   | **Build Command** | Leave empty |
   | **Publish Directory** | . (current directory) |

4. Click "Create Static Site"
5. Your frontend URL: `https://chatbot-ui.onrender.com`

### Option B: Deploy on Vercel (Alternative)

1. Go to https://vercel.com
2. Import GitHub repository
3. Click "Deploy"
4. Update `index.html` API URL to your Render backend

### Option C: Deploy Both Services Together

Create a single service that serves both frontend and backend:

**Update main.py to serve static files:**
```python
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Add at the end of main.py before if __name__ == "__main__":
app.mount("/", StaticFiles(directory=".", html=True), name="static")
```

## Step 6: Verify Deployment

### Check Backend
```
https://chatbot-api.onrender.com/health
```
Expected response:
```json
{"status": "healthy", "service": "chatbot-api"}
```

### Check Frontend
Open `https://chatbot-ui.onrender.com` in browser

### Test Chat
- Type a question
- Should see bot response
- Check browser console (F12) for any errors

## 📊 Monitoring & Logs

### View Logs in Render
1. Go to your service dashboard
2. Click "Logs" tab
3. See real-time logs

### Enable Notifications
- Settings → Notifications
- Email alerts for deployment issues

## 💰 Costs

| Tier | Cost | Includes |
|------|------|----------|
| **Free** | $0/month | 750 hours/month (1 service), 100 GB bandwidth |
| **Starter** | $7/month | Always-on, better specs |
| **Standard** | $25/month | Priority support, scaling |

**Tip:** Free tier will spin down after 15 min of inactivity.

## 🔧 Common Issues

### Backend Timeout on Render Free Tier
- Solution: Upgrade to Starter tier
- Or: Reduce knowledge base size
- Or: Add response caching

### CORS Errors
- Already handled in `main.py`
- Check that API_URL in `index.html` matches Render URL

### 502 Bad Gateway
- Check build command
- Check start command
- View logs for errors

### Slow Response Times
- Likely due to free tier cold start
- Upgrade to Starter+ tier
- Add more keywords to knowledge base for faster matching

## 🔄 Continuous Deployment

After initial deployment, every push to GitHub will automatically redeploy:

```powershell
# Make changes
git add .
git commit -m "Update knowledge base"
git push
# Render auto-deploys!
```

## 📈 Scaling

As your chatbot grows:

1. **Upgrade to Starter tier** for always-on service
2. **Add PostgreSQL database** instead of JSON
3. **Implement caching** with Redis
4. **Use CDN** for frontend assets
5. **Add authentication** for admin panel

## 🎓 Learning Resources

- Render Docs: https://render.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- Python Deployment: https://render.com/docs/deploy-python

---

## 🎉 You're Live!

Your chatbot is now accessible globally at:
- **Frontend:** https://chatbot-ui.onrender.com
- **Backend:** https://chatbot-api.onrender.com
- **API Docs:** https://chatbot-api.onrender.com/docs

Share the link with others! 🚀
