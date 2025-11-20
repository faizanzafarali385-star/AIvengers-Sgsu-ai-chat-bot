import http.server
import socketserver
import os
from pathlib import Path

# Change to the directory containing the HTML file
os.chdir(Path(__file__).parent)

PORT = 8080
HANDLER = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), HANDLER) as httpd:
    print(f"Frontend server running at http://localhost:{PORT}")
    print(f"Backend API running at http://localhost:8000")
    print(f"Open http://localhost:{PORT} in your browser")
    httpd.serve_forever()
