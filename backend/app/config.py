"""Configuration settings for SGSU Chatbot."""
import os
from pathlib import Path

# Paths
APP_DIR = Path(__file__).resolve().parent
BACKEND_DIR = APP_DIR.parent
BASE_DIR = BACKEND_DIR.parent
DATA_DIR = BACKEND_DIR / "data"
FRONTEND_DIR = BASE_DIR / "frontend"

# Knowledge base file path with fallback
KNOWLEDGE_BASE_PATH = DATA_DIR / "knowledge_base.json"
if not KNOWLEDGE_BASE_PATH.exists():
    fallback = BASE_DIR / "knowledge_base.json"
    if fallback.exists():
        KNOWLEDGE_BASE_PATH = fallback

# Server settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", "8080"))

# OpenRouter API settings
OPENROUTER_API_URL = os.getenv(
    "OPENROUTER_API_URL", 
    "https://openrouter.ai/api/v1/chat/completions"
)

# OpenRouter API Keys - supports comma-separated list or fallback keys
env_keys = os.getenv("OPENROUTER_API_KEY")
if env_keys:
    OPENROUTER_API_KEYS = [k.strip() for k in env_keys.split(",") if k.strip()]
else:
    OPENROUTER_API_KEYS = [
        "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",
        "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"
    ]

USE_OPENROUTER = os.getenv("USE_OPENROUTER", "true").lower() in ("true", "1", "yes")
