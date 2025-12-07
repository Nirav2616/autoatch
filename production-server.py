#!/usr/bin/env python3
import http.server
import socketserver
import os
import json
from urllib.parse import urlparse

PORT = 8080

class ProductionHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="dist/public", **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Parse the URL
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Handle React routing - serve index.html for all routes
        if path == '/' or path.startswith('/editor') or path.startswith('/app'):
            self.serve_react_app()
            return
        
        # Handle API routes
        if path.startswith('/api/'):
            self.handle_api(path)
            return
        
        # Default to serving static files from dist/public
        super().do_GET()
    
    def serve_react_app(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Read and serve the built React index.html
        try:
            with open('dist/public/index.html', 'r', encoding='utf-8') as f:
                content = f.read()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            # Fallback HTML
            html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ArchSense</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }
        .container {
            text-align: center;
            background: rgba(255,255,255,0.1);
            padding: 2rem;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        .error { color: #ff6b6b; font-size: 2rem; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <div class="container">
        <div class="error">⚠️ Error</div>
        <h1>🏗️ ArchSense</h1>
        <p>Built files not found. Please run 'npm run build' first.</p>
    </div>
</body>
</html>'''
            self.wfile.write(html.encode('utf-8'))
    
    def handle_api(self, path):
        if path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'OK',
                'message': 'ArchSense Production API is running',
                'frontend': 'Built React app loaded',
                'backend': 'Python server active'
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'API endpoint not found'}).encode())

# Change to the script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with socketserver.TCPServer(("", PORT), ProductionHandler) as httpd:
    print("=" * 60)
    print(f"🚀 ARCHSENSE PRODUCTION SERVER RUNNING")
    print(f"📍 URL: http://localhost:{PORT}")
    print(f"⚛️  Frontend: Built React application")
    print(f"🐍 Backend: Python HTTP server")
    print(f"🔗 API: http://localhost:{PORT}/api/health")
    print("=" * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.shutdown()
