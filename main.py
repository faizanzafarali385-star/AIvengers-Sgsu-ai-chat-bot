"""Entrypoint for the SGSU Chatbot Application."""
import uvicorn
from backend.app.api import app
from backend.app.config import HOST, PORT

# Expose app for ASGI servers like uvicorn main:app
__all__ = ["app"]

if __name__ == "__main__":
    print(f"🚀 Starting SGSU Chatbot on http://{HOST}:{PORT}")
    print(f"💡 Frontend & API available at http://localhost:{PORT}")
    uvicorn.run("backend.app.api:app", host=HOST, port=PORT, reload=True)
