"""Development server to serve only the frontend independently on port 8080."""
import http.server
import socketserver
import os
from pathlib import Path

# Change to the frontend directory
frontend_dir = Path(__file__).resolve().parent / "frontend"
if frontend_dir.exists():
    os.chdir(frontend_dir)
else:
    os.chdir(Path(__file__).resolve().parent)

PORT = 8080
HANDLER = http.server.SimpleHTTPRequestHandler

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), HANDLER) as httpd:
        print(f"🌐 Frontend server running at http://localhost:{PORT}")
        print(f"⚙️  Backend API expected at http://localhost:8000")
        print(f"👉 Open http://localhost:{PORT} in your browser")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down frontend server.")
