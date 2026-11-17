FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY main.py .
COPY serve_frontend.py .

# Expose ports
EXPOSE 8000 8080

# Run the FastAPI server (serves both API and frontend UI)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
